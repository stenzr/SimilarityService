# Similarity Service

A Rest API to detect the similarity between two sentences.

</br>

---

</br>

## Authors

- [Rohit Kumar @stenzr](https://github.com/stenzr)

</br></br>

---

</br>

## Tech Stack

**Server:** Flask \
**Language:** Python \
**Database:** MongoDb \
**Container:** Docker, Docker-Compose \
**ML:** Spacy
</br></br>

---

</br>

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

</br></br>

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

</br></br>

#### Refill the user specific tokens

```http
  POST /refill
```

| Parameter  | Type      | Description                               |
| :--------- | :-------- | :---------------------------------------- |
| `username` | `string`  | **Required**. username to validate user   |
| `admin_pw` | `string`  | **Required**. admin password              |
| `refill`   | `integer` | **Required**. the number of tokens to add |

## <br/></br>

</br>

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
