from locust import HttpUser, TaskSet, task, between

class MyTask(TaskSet):
    
    @task(5)
    def form(self):
        self.clien


class WebsiteUser(HttpUser):
    wait_time = between(1,5)
    
    @task
    def index_page(self):
        self.client.get(url="/hello")