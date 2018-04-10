import React, { Component } from 'react';

let ctx;
let img;

class Camera extends Component {
  componentDidMount() {

    this.connection = new WebSocket('ws://localhost:8888');
    //this.connection.binaryType="arraybuffer";
    this.connection.onmessage = evt => {
      // console.log("ws="+evt.data+" type="+typeof(evt.data))
      var blob = new Blob( [ evt.data ], { type: "image/png" } );
      var urlCreator = window.URL || window.webkitURL;
      var imageUrl = urlCreator.createObjectURL( blob );
      img.src = imageUrl;

  }
  // const canvas = this.refs.canvas
  //ctx = canvas.getContext("2d")
  var img = this.refs.img;
  }
  render() {
  let imgSrc ="data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";
    return(
      <div style={{display: 'flex', justifyContent: 'center'}}>
      <div style={{display: 'flex', justifyContent: 'center', border: '1px solid red'}}>
      <img ref="img" key="imgkey" src={imgSrc} />
      </div></div>
    )
  }
}
export default Camera
