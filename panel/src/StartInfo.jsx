import React, { Component } from 'react';
import {Route, Link } from "react-router-dom"

export default class StartInfo extends Component {
  componentDidMount(){
    console.log("mount comp2");
  }
  render() {
    //<Camera text="tick=0" ></Camera>
    // <ListPhotos></ListPhotos>
    // <p style={{display: 'flex', justifyContent: 'center'}}><b> Video from web camera.</b></p>
    return (
      <div>
        <h1>About</h1>
        <p>Bell server app find people on the photo by existing photos. </p>
        <p>If you want check list existing photos or add photo for recognition please go to pages with <Link to="/faceList">Faces</Link>. </p>
        <p>If you want to find people on the photo please go to page <Link to="/recognation">Recognation</Link></p>
      </div>
    )}
  }
