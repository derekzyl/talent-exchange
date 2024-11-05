# FLOW PROJECT

the flow project is an app that renders not just digital skills but also technical skills needed by a customer
the idea is a platform where all services are being rendered.

## Tech and Stack used
### Backend


   1. <img src ="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width= 100px />
   2. <img src ="https://www.sqlalchemy.org/img/sqla_logo.png" width= 100px />
   2. <img src ="https://docs.pydantic.dev/logo-white.svg" width= 100px height="20px" />




## API endpoints

### Auth endpoint

- type of request: **POST**
- structure of incoming data: {
    name,
    email,
    password,
    confirm password
}
- response: {
    message,
    token,
    status
}
- code example:

```python

curl -x POST baseurl/signup
     -H "content-type:application/json"
     -d {name, email, password, confirm password}
```


