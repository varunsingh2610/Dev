#=================================================================================================================
#=================================================================================================================
import falcon
import json
import base64
from collections import OrderedDict

#=================================================================================================================

from ..model.db_base import Session, engine, Base
from ..model.movies import User

#=================================================================================================================
#=================================================================================================================

class CreateUser():
	def on_post(self, req, resp):
		
		try:
			db = Session()
			raw_json = req.stream.read()
			raw_data = json.loads(raw_json.decode("utf-8"))

			username = raw_data['username']			
			password = raw_data['password']
			adminrole = raw_data['admin_role']

			user_basic_token = bytes(str(username)+":"+str(password), "utf=8")
			basic_token = (base64.b64encode(user_basic_token)).decode("utf-8")
			create_user = dict(username=username, password=password, basic_auth=basic_token, admin_role=adminrole, user_status="Active")
			user_exist = db.query(User).filter(User.username.ilike(username.strip())).first()
			userdata = User(**create_user)

			if not user_exist:
				db.add(userdata)
				output = {'Status': falcon.HTTP_200, 'Message': "User account created, Your Basic Authorization token: "+ basic_token}
				resp.status = falcon.HTTP_200
				resp.body = json.dumps(output)
				db.commit()
			else:
				resp.body = json.dumps({"Status": falcon.HTTP_400, "Error":"Username already exist: "+username})
				resp.status = falcon.HTTP_400
				return resp

		except (KeyError, ValueError) as e:
			db.rollback()
			error = "{err} field is required..!".format(err=e)
			resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(error)})
			resp.status = falcon.HTTP_400

		except Exception as e:
			db.rollback()
			resp.body = json.dumps({"Status": falcon.HTTP_400, 'Error':str(e)})
			resp.status = falcon.HTTP_400
			return resp

		finally:
			db.close()
			
#=================================================================================================================
#=================================================================================================================
