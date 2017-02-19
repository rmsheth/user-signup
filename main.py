#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        label {margin:25px 0px 0px 0px;}
        input {float;left;}
        .error {float:right;color:red;display:inline;}
        .clear {clear:both;}
    </style>
</head>
<body>
    <h3>
        <a href="/">Signup</a>
    </h3>
"""

signup_form = """
	<form action="/" method="POST" class="form">
	    <table>
	        <tr>
	            <td><label>Username:</td>
	            <td><input type="text" name="username" value="" /></td>
	            <td><span class="error"> %(e_username)s</span></td>
	            </label>
	        </tr>
	        <tr>
	            <td><label>Password:</td>
	            <td><input type="password" name="password" value="" /></td>
	            <td><span class="error"> %(e_password)s</span</td>
	            </label>
	        </tr>
	        <tr>
	            <td><label>Verify Password:</td>
	            <td><input type="password" name="verify" value="" /></td>
	            <td><span class="error"> %(e_verify)s</span></td>
	            </label>
	        </tr>
	        <tr>
	            <td><label>Email(optional):</td>
	            <td><input type="text" name="email" value="" /></td>
	            <td><span class="error"> %(e_email)s</span></td>
	            </label>
	        </tr>
	    </table>
	    <input type="submit" value="Submit" /><br />
	</form>
	"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def build_page(self, e_username="", e_password="", e_verify="", e_email="", username="", password="", verify="", email=""):
        self.response.write(page_header + signup_form % {"e_username": e_username,
                                                "e_password": e_password,
                                                "e_verify": e_verify,
                                                "e_email": e_email,
                                                "username": username,
                                                "password": password,
                                                "verify": verify,
                                                "email": email})

    def get(self):
        self.build_page()

    def post(self):
        username_req = self.request.get("username")
        password_req = self.request.get("password")
        verify_pass_req = self.request.get("verify")
        email_req = self.request.get("email")

        if username_req == '':
            e_username = "You must create a user name"
            self.build_page(e_username)
        elif not valid_username(username_req):
            e_username = "You must create a valid user name"
            self.build_page(e_username)
        elif password_req == '':
            e_password = "You must create a password"
            self.build_page(e_password)
        elif not valid_password(password_req):
            e_password = "That's not a valid password"
            self.build_page(e_password)
        elif verify_pass_req == '':
            e_verify = "You must create a matching password"
            self.build_page(e_verify)
        elif verify_pass_req != password_req:
            e_verify = "Your passwords do not match"
            self.build_page(e_verify)
        elif email_req != '' and not valid_email(email_req):
            e_email = "That's not a valid email, dude"
            self.build_page(e_verify)
        else:
            success = "Welcome, " + username_req
            greeting = "<h1>" + success + "</h1>"
            self.response.write(greeting)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
