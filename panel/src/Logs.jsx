import React from 'react';
import {Table, Nav, NavItem, Panel, Tooltip, OverlayTrigger , Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'

export default class Logs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      imageURL: '',
      result:"",
      resultTr: false,
      alertType:"info"
    };
    this.text = "Loading data..."
    this.activeKey='../log/webServer.log'
  }
  componentDidMount() {
    this.resultTr=false;
    this.takeLogData()
  }

  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  takeLogData(){
      fetch(this.activeKey)
      .then(this.handleErrors)
      .then((response) => {
        // console.log("server ansver0=",response)
        response.text().then((body) => {
          // console.log("server body=",body)
          let strHtml= body.replace(/(?:\r\n|\r|\n)/g, '<br />');
          strHtml = strHtml.replace(/<img/g,"<img width=\"64\" height=\"64\" ")
          this.refs.log_body.innerHTML = strHtml
          this.setState({ resultTr: !this.state.resultTr});
          // this.setState({alertType:body.Type})
        });
      })
      .catch((err)=>{console.log("Error connect to Server") })
}
  clearLog(){
    fetch('../clearLog?'+this.activeKey)
    .then(this.handleErrors)
    .then((response) => {
      // console.log("server ansver0=",response)
      this.takeLogData();
    })
    .catch((err)=>{console.log("Error connect to Server") })
  }

  handleSelectTab(k){
    // console.log("tab click",k)
    this.activeKey = k
    this.takeLogData()
    this.state.resultTr = !this.state.resultTr
  }

  render() {
    return (
      <div>
        {this.state.resultTr}
        <div style={{fontSize:"200%"}} >Logs &nbsp;&nbsp;<Button bsStyle="primary" onClick={this.clearLog} name ="btUpdate" key ="bt" >Clear log</Button></div>
          <Nav bsStyle="tabs" activeKey={this.activeKey} onSelect={k => this.handleSelectTab(k)}>
          <NavItem eventKey='../log/webServer.log' >Server</NavItem>
          <NavItem eventKey='../log/camera_webCamera_face.log' >Events</NavItem>
          <NavItem eventKey='../log/camera_webCamera.log' >Camera</NavItem>
          <NavItem eventKey='../log/camera_manager.log' >Cameras manager</NavItem>
        </Nav>
        <div key="log_body" ref="log_body" id="log_body"> </div>

      </div>
    )}
}
