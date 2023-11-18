from unittest import TestCase
from app import app
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserPageTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        user = User(first_name= 'test_first_name', last_name = 'test_last_name' ,image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTo6wvCv5V-p7-_dlcTR0C-vLpnzlu3grPKIOZCHvg&s' )
        db.session.add(user)
        db.session.commit()

        self.user_id= user.id

    def tearDown(self):
        db.session.rollback()

    def test_user_list(self):
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code , 200)
            self.assertIn('test_first_name', html)

    def test_creat_page(self):
        with app.test_client() as client:
            res = client.get("/users/new")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Create User" , html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {'first_name' : 'sam' , 'last_name': 'willow' , 'image_url' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTo6wvCv5V-p7-_dlcTR0C-vLpnzlu3grPKIOZCHvg&s'}
            res = client.post("/add_to_db", data= data, follow_redirects =True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code , 200)
            self.assertIn("sam" , html)

    def test_show_detals(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("test_last_name" , html)

    def test_edit_user(self):
        with app.test_client() as client:
            data = {'first_name' : 'Tank' , 'last_name': 'Halls' , 'image_url' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTo6wvCv5V-p7-_dlcTR0C-vLpnzlu3grPKIOZCHvg&s'}
            res = client.post(f'/users/{self.user_id}/edit', data= data, follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code , 200)
            self.assertIn("Tank Halls" , html)
            self.assertNotIn("test_first_name", html)

    def test_delete(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/delete', follow_redirects =True)
            html = res.get_data(as_text =True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn("test_first_name" , html)



            