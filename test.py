
import unittest
import os
from flaskblogg import app
from flaskblogg.models import db, Author, Post

#Restrict permissions from USER
#Allow user to read all, create post, delete own post, edit own post
#Allow Admin to read all, create post, delete own post, edit own post, delete anyone posts, restrict editing someone's post

SECRET_KEY=os.environ.get('SECRET_KEY')
database_name = "blogatog"

project_dir = os.path.dirname(os.path.abspath(__file__))
database_path='postgres://epixojdhlwjsir:99617ba473d3f6609a9c93439e87bb31fb1ac9fa6d5d167e66e2e29d703261f0@ec2-52-71-153-228.compute-1.amazonaws.com:5432/d93kgv3fnkj0fg'

User = os.getenv('User')
Admin = os.getenv('Admin')


def set_auth_header(role):
    if role == 'User':
        return {'Authorization': 'Bearer {}'.format(User)}
    elif role == 'Admin':
        return {'Authorization': 'Bearer {}'.format(Admin)}
#######



class MainTestCase(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.app = app.test_client()
        # db.drop_all()
        # db.create_all()

    # # blog endpoint tests

    def test_author_id(self):
        res = self.app.get(
            '/api/author/1/', headers=set_auth_header('User'))
        self.assertEqual(res.status_code, 401)

    def test_author_id(self):
        res = self.app.get(
            '/api/author/2/', headers=set_auth_header('Admin'))
        self.assertEqual(res.status_code, 401)

    def test_delete(self):
        res = self.app.get(
            '/api/post/1/remove', headers=set_auth_header('User'))
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        res = self.app.get(
            '/api/post/2/remove', headers=set_auth_header('Admin'))
        self.assertEqual(res.status_code, 405)

    def test_register(self):
        res = self.app.get(
            '/register', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_register(self):
        res = self.app.get(
            '/register', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_dashboard(self):
        res = self.app.get(
            '/dashboard', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_dashboard(self):
        res = self.app.get(
            '/dashboard', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_allposts(self):
        res = self.app.get(
            '/all-posts', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_allposts(self):
        res = self.app.get(
            '/all-posts', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_new(self):
        res = self.app.get(
            '/post/new', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_new(self):
        res = self.app.get(
            '/post/new', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_post1(self):
        res = self.app.get(
            '/post/1', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_post1(self):
        res = self.app.get(
            '/post/1', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_post1remove(self):
        res = self.app.get(
            '/post/1/remove', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)

    def test_post1remove(self):
        res = self.app.get(
            '/post/1/remove', headers=set_auth_header('session'))
        self.assertEqual(res.status_code, 200)    
    # def test_get_movies_unauthorized(self):
    #     res = self.app.get(
    #         '/movies', headers=set_auth_header(''))
    #     self.assertEqual(res.status_code, 401)


    # def test_add_movie(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }

    #     res = self.app.post(
    #         '/movies', json=data, headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(res.get_json()['success'], True)



    # def test_add_movie_fail(self):
    #     res = self.app.post(
    #         '/movies', json={}, headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(res.get_json()['success'], False)



    # def test_add_movie_unauthorized(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     res = self.app.post(
    #         '/movies', json=data, headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')



    # def test_edit_movie(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post('/movies', json=data,
    #                   headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id
    #     res = self.app.patch(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.get_json()['success'], True)



    # def test_edit_movie_unauthorized(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post('/movies', json=data,
    #                   headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id
    #     res = self.app.patch(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')



    # def test_edit_movie_fail(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post('/movies', json=data,
    #                   headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id

    #     data = {
    #         "title": '',
    #         "release_date": ''
    #     }
    #     res = self.app.patch(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 400)



    # def test_delete_movie(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post(
    #         '/movies', json=data, headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id
    #     res = self.app.delete(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.get_json()['success'], True)




    # def test_delete_movie_unauthorized(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post(
    #         '/movies', json=data, headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id
    #     res = self.app.delete(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('Admin'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')

    # # actors endpoint tests




    # def test_get_actors(self):
    #     res = self.app.get(
    #         '/actors', headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 200)




    # def test_get_actors_unauthorized(self):
    #     res = self.app.get(
    #         '/actors', headers=set_auth_header(''))
    #     self.assertEqual(res.status_code, 401)




    # def test_add_actor(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     res = self.app.post(
    #         '/actors', json=data, headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(res.get_json()['success'], True)




    # def test_add_actor_fail(self):
    #     res = self.app.post(
    #         '/actors', json={}, headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(res.get_json()['success'], False)




    # def test_add_actor_unauthorized(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     res = self.app.post(
    #         '/actors', json=data, headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')





    # def test_edit_actor(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.patch(
    #         f'/actors/{actor_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.get_json()['success'], True)





    # def test_edit_actor_unauthorized(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.patch(
    #         f'/actors/{actor_id}', json=data,
    #         headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')





    # def test_edit_actor_fail(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.patch(
    #         f'/actors/{actor_id}', data={},
    #         headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')





    # def test_delete_actor(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.delete(
    #         f'/actors/{actor_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.get_json()['success'], True)





    # def test_delete_actor_unauthorized(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.delete(
    #         f'/actors/{actor_id}', json=data,
    #         headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
    unittest.main()