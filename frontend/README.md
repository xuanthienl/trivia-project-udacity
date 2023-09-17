Trivia API - Frontend
-----

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── public
  │   ├── index.html
  ├── src
      ├── components 
      ├── stylesheets
      ├── App.js
      ├── App.test
      ├── index.js
  ```

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

## Setting up the Frontend

First, [install Node](https://nodejs.com/en/download) if you haven't already.

1. Installing project dependencies:
  
  This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

  ```
  $ npm install
  ```

  _tip_: `npm i`is shorthand for `npm install``

2. Run the Server:

  The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

  Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

  ```
  $ npm start
  ```
