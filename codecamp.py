import os
import re
import tornado
import tornado.httpserver
import tornado.autoreload
import tornado.escape
import tornado.httpclient
import tornado.ioloop
import tornado.web
import simplejson as json
import random
import logging
import uuid
from lib import shred

from utils.custom_exceptions import IndentError
        
TEMPLATE_FILEPATH = 'static/templates/shred.template'
REVERSED_IMAGE_FILEPATH = 'static/assets/koi-reversed.png'
UNREVERSED_IMAGE_FILEPATH = 'static/assets/user_image_storage/koi-unreversed'
PRE_CODE_CONTENT_FILEPATH = 'static/templates/pre_code.txt'
USER_CODE_CONTENT_FILEPATH = 'static/templates/user_code.txt'
INVALID_WORDS = ['exec', 'eval', 'import', 'execfile', '__' 'init']
MAX_ACCEPTED_LENGTH = 500


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = str(uuid.uuid4())
        pre_code_content, pre_code_num_lines = self.get_pre_code_content()
        user_code_starting_content = self.get_user_code_starting_content()
        return self.render_template(template=TEMPLATE_FILEPATH,
                    pre_code_content=pre_code_content,
                    pre_code_num_lines=pre_code_num_lines,
                    user_code_starting_content=user_code_starting_content,
                    image=REVERSED_IMAGE_FILEPATH, 
                    user_id=user_id)
    
    def post(self):
        message = ''
        image = REVERSED_IMAGE_FILEPATH
        is_correct = False
        user_code_raw = self.get_argument("user_code", None)
        user_id = self.get_argument("user_id", None)
        pre_code_content, pre_code_num_lines = self.get_pre_code_content()
        
        is_safe = self.check_safety(user_code_raw)
        
        try:
            user_code = self.format_code(user_code_raw)
        except Exception, e:
            error_message = str(e) 
            return self.render_template(template=TEMPLATE_FILEPATH,
                                pre_code_content=pre_code_content,
                                pre_code_num_lines=pre_code_num_lines,
                                user_code_starting_content=user_code_raw,
                                image=image, 
                                user_id=user_id,
                                message=error_message)
            
            
        if user_code and is_safe:
            # Compile user's code
            try:
                is_correct = shred.unreverse_image(user_code, user_id)
                image = UNREVERSED_IMAGE_FILEPATH + "-" + user_id + ".png"
                # cache buster
                image += "?v=%s" % int(random.randint(10000,99999))
            except Exception, e:
                error_message = str(e)
                return self.render_template(template=TEMPLATE_FILEPATH,
                                    pre_code_content=pre_code_content,
                                    pre_code_num_lines=pre_code_num_lines,
                                    user_code_starting_content=user_code_raw,
                                    image=image, 
                                    user_id=user_id,
                                    message=error_message)

        if is_correct:
            print "is_correct"
            print is_correct
            message = "Booyah! Saved them fishes. Well done."
        
        # Render the template
        return self.render_template(template=TEMPLATE_FILEPATH,
                    pre_code_content=pre_code_content,
                    pre_code_num_lines=pre_code_num_lines,
                    user_code_starting_content=user_code_raw,
                    image=image, 
                    user_id=user_id,
                    message=message,
                    user_code=user_code, 
                    is_safe=is_safe)
    
    def get_user_code_starting_content(self):
        """Returns the code that the user sees in their textarea
        upon page load
        """
        uc_file = open(USER_CODE_CONTENT_FILEPATH, 'r')
        uc_content = uc_file.read()
        uc_file.close()
        return uc_content
            
    def get_pre_code_content(self):
        """Gets the python code that will go into 
        the pre_code block in the html template
        """
        pc_file = open(PRE_CODE_CONTENT_FILEPATH, 'r')
        pc_content = pc_file.read()
        pc_file = open(PRE_CODE_CONTENT_FILEPATH, 'r')
        pc_num_lines = len(pc_file.readlines())
        pc_file.close()
        return pc_content, pc_num_lines
    
    def check_safety(self, user_code=None):
        is_safe = True
        if len(user_code) > MAX_ACCEPTED_LENGTH:
            return False
            
        for w in INVALID_WORDS:
            if user_code.find(w) != -1:
                is_safe = False
                break
        return is_safe
    
    def format_code(self, user_code=None):
        if not user_code:
            return None
        lines = user_code.split("\n")
        lines = lines[1:-1]
        
        lines_without_first_indent = []
        for line in lines:
            if line[0:4] != '    ':
                print "indentation error"
                raise IndentError('Indentation is important in python; make sure your lines are indented correctly.')
            else:
                lines_without_first_indent.append(line[4:])
        user_code = '\n'.join(lines_without_first_indent)
        return user_code
        
    def render_template(self,
                        template,
                        pre_code_content,
                        pre_code_num_lines,
                        user_code_starting_content,
                        image, 
                        user_id, 
                        user_code=None, 
                        is_safe=None,
                        message=''):
                        
        if message:
            print "backslashing"
            message = message.replace("'", "\\'")
            message = message.replace('"', '\\"')
            print message
        
        self.render(template,
                    pre_code_content=pre_code_content,
                    pre_code_num_lines=pre_code_num_lines,
                    user_code_starting_content=user_code_starting_content,
                    image=image, 
                    user_id=user_id, 
                    user_code=user_code, 
                    is_safe=is_safe,
                    message=message)
    
settings = {
    'debug': True, # enables automatic reruning of this file when edited
    'static_path': os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler)
    ],  
     **settings)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9001)
    tornado.ioloop.IOLoop.instance().start()
