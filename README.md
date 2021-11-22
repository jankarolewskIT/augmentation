# augmented_img_API

<h1>To test my application fallow these instructions<h1/>

In your terminal:
1. Clone this repository
    type: git clone <this repo name>
2. change directory to "augmented_img_API" and 
    type: docker-compose up
3. Enter your web_container
    type: docker exec -it <container ID> bash
4. Run migrations 
    type: python manage.py migrate
5. Load data for testing
    5.1 Load test image:
    type: python images/loaders/test_image_loader.py 
    5.2 Parse Image to test response JSON file:
    type: python images/loaders/request_data_loader.py 
6. Run tests:
    type: python manage.py test


Though not every test passes the TestCase, converted images are stored in media/img/ directory and their instances are saved on the Postgres database. 

In my opinion, this may be related to some caveats with base64 or converting images with PIL.Image(). While testing with Postman, no troubles have occurred, and double/triple/etc. convetrions were possible. I will fix these tests in the future. 
