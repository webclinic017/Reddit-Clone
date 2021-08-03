import React from 'react';
import NavBar from '../general/NavBar';
import PostFeed from '../posts/PostFeed';
import '../../styles/homeScreen.css';

function HomeScreen() {
  return (
    <div className="homeScreen">
      <NavBar />
      <div className="homeScreen__main">
        <div className="homeScreen__left"></div>
        <div className="homeScreen__middle">
          <PostFeed groupName="feed" />
        </div>
        <div className="homeScreen__right"></div>
      </div>
    </div>
  );
}

export default HomeScreen;
