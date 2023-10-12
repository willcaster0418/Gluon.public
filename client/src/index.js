import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
//import { GoogleOAuthProvider } from '@react-oauth/google';

const root = ReactDOM.createRoot(document.getElementById('root'));
//root.render(
//    <GoogleOAuthProvider clientId="105029058318-c9687kbih56lupv3ll8lorrbfsfccnme.apps.googleusercontent.com">
//        <App/>
//    </GoogleOAuthProvider>);

root.render(<App/>)