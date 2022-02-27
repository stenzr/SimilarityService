# Similarity Service

A Rest API to detect the similarity between two sentences.


----


## Authors

- [Rohit Kumar @stenzr](https://github.com/stenzr)

</br>

----



## Tech Stack

**Server:** Flask \
**Language:** Python \
**Database:** MongoDb \
**Container:** Docker, Docker-Compose \
**ML:** Spacy
</br></br>

----


## API Reference

</br>

#### Register a new user

```http
  POST /register
```

| Parameter  | Type     | Description                        |
| :--------- | :------- | :--------------------------------- |
| `username` | `string` | **Required**. username to register |
| `password` | `string` | **Required**. password of the user |

</br>

#### Sample Request

````json
{
    "username": "user2",
    "password": "user_password"
}
````
#### Sample Response

````json
{
    "msg": "Sign up Successful",
    "results": {
        "similarity": null
    },
    "status": 200,
    "userInformation": {
        "currentTokens": 6,
        "username": "user2"
    }
}

````

</br>

#### Detect similarity between two texts

```http
  POST /detect
```

| Parameter  | Type     | Description                             |
| :--------- | :------- | :-------------------------------------- |
| `username` | `string` | **Required**. username to validate user |
| `password` | `string` | **Required**. password of the user      |
| `text1`    | `string` | **Required**. Sentence1                 |
| `textt2`   | `string` | **Required**. Sentence2                 |

</br>

#### Sample Request

````json
{
    "username": "user2",
    "password": "user_password",
    "text1" : "you have ",
    "text2" : "You My Have "
}
````
#### Sample Response

````json
{
    "msg": "Success",
    "results": {
        "similarity": 53.80624762110769
    },
    "status": 200,
    "userInformation": {
        "currentTokens": 5,
        "username": "user2"
    }
}

````

</br>

#### Refill the user specific tokens

```http
  POST /refill
```

| Parameter  | Type      | Description                               |
| :--------- | :-------- | :---------------------------------------- |
| `username` | `string`  | **Required**. username to validate user   |
| `admin_pw` | `string`  | **Required**. admin password              |
| `refill`   | `integer` | **Required**. the number of tokens to add |

</br>

#### Sample Request

````json
{
    "username": "user2",
    "admin_pw": "admin_password",
    "refill" : 10
}
````
#### Sample Response

````json
{
    "msg": "Success",
    "results": {
        "similarity": null
    },
    "status": 200,
    "userInformation": {
        "currentTokens": 15,
        "username": "user2"
    }
}

````

</br>

----



## Build Details:

</br></br>

#### To build the project on your system

</br>

- [x] Open your terminal in the required directory
      </br></br>

- [x] Clone the repository

```bash
  git clone git@github.com:stenzr/SimilarityService.git
```

</br>

- [x] CD to the project directory

```bash
  cd SimilarityService
```

</br>

- [x] Build the docker images

```bash
  sudo docker-compose build
```

</br>

- [x] Start the Services

```bash
  sudo docker-compose up
```

</br>

- [x] The server starts on localhost:5000
      </br></br>

- [x] Use Postman to send request to the endpoints
      </br></br>

---
