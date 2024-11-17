import React from 'react';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { auth } from './firebase';
import { toast } from "react-toastify";

const SignInWithGoogle = () => {
  function GoogleLogin() {
    const provider = new GoogleAuthProvider();
    signInWithPopup(auth, provider).then(async (result) => {
      if (result.user) {
        localStorage.setItem('userName', result.user.displayName);
        localStorage.setItem('userPhoto', result.user.photoURL);

        toast.success("User login successful", {
          position: "top-center",
        });
        window.location.href = "/main";
      }
    });
  }

  return (
    <div>
      <button 
        onClick={GoogleLogin} 
        className="bg-[#335AE2] w-full h-20 text-white py-2 px-4 rounded-3xl"
      >
        Sign In
      </button>
    </div>
  );
};

export default SignInWithGoogle;
