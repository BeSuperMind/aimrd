// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBM8aesPETO9q4hLQCDyIbOXFARVqZtPUU",
  authDomain: "login2-9880b.firebaseapp.com",
  projectId: "login2-9880b",
  storageBucket: "login2-9880b.firebasestorage.app",
  messagingSenderId: "117309935089",
  appId: "1:117309935089:web:3cc0f2bb096e9795b38850"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth();