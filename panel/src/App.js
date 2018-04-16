import React, { Component } from 'react'
// import {Navbar, Nav,MenuItem, NavDropdown , NavItem} from 'react-bootstrap'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import {Route, Link} from "react-router-dom"
// import { useRouterHistory } from 'react-router'
import { LinkContainer } from 'react-router-bootstrap';



import Camera from './Camera'
import Upload from './Upload'
import ListPhotos from './ListPhotos'
import ListCameras from './ListCameras'
import Recognation from './Recognation'
import Config from './Config'
import Logs from './Logs'
import Login from './Login'
import Notify from './Notify'
import StartInfo from './StartInfo'
import EditFace from './EditFace'
import EditCamera from './EditCamera'
import {Table, Nav,Navbar, Pager, NavDropdown,  NavItem, Panel, Tooltip, OverlayTrigger , Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';

import AuthService from './AuthService'
import createBrowserHistory from "history/createBrowserHistory"

const history = createBrowserHistory({
  forceRefresh: true
})

var counter = 0
var ctx

export default class App extends Component {
  constructor(props) { super(props)
    this.state = { login: "Login", actionTr:false}
    this.Auth = localStorage.getItem('id_token')
  }

  componentWillMount(){
   // console.log("Auth update=",localStorage.getItem('id_token'))
    if(this.Auth){ this.setState({login:"Logout"})
    }else{this.setState({login:"Login"})
    }
    console.log("ddd",this.props.history)
  }

  componentDidMount(){

    // console.log("mount App",this.Auth)
    // if (!this.Auth.loggedIn()) {
    //     // this.props.history.replace('/login')
    // }
    // else {
    //     try {
    //         const profile = this.Auth.getProfile()
    //         console.log("profile",profile)
    //         this.setState({
    //             user: profile
    //         })
    //     }
    //     catch(err){
    //         this.Auth.logout()
    //         // this.props.history.replace('/login')
    //     }
    // }
  }

  // onMenuSelect(ev){ //ev.preventDefault()
  //   console.log("ev=",ev)
  // }

  showContent(){
    console.log("Auth show=", this.Auth)
    if(this.Auth){
      return(
        <div>
          <Route exact={true} path="/" component={StartInfo}/>
          <Route path="/recognation" component={Recognation}/>
          <Route path="/facesList" component={ListPhotos}/>
          <Route path="/camerasList/" component={ListCameras}/>
          <Route path="/config" component={Config}/>
          <Route path="/notify" component={Notify}/>
          <Route path="/log" component={Logs}/>
          <Route path="/editFace/:id" component={EditFace}/>
          <Route path="/editCamera/:id" component={EditCamera}/>
        </div>
      )
    }
    else{
      return(
        <div style={{textAlign: "center"}}>
          <div style={{color:"red",fontSize:"200%"}}>Please login</div>
          <Route path="/login" component={Login}/>
        </div>)
    }
  }

  doLogin(){
    console.log("start login",this.Auth )
    if(this.Auth){
      localStorage.removeItem('id_token')
      this.Auth = 0
      this.setState({login:"Login"})
    }else{this.setState({login:"Logout"})}
    history.push("/login")
    window.location.reload()
  }
  
  render() {
    //<Camera text="tick=0" ></Camera>
    // <ListPhotos></ListPhotos>
    // <p style={{display: 'flex', justifyContent: 'center'}}><b> Video from web camera.</b></p>
      // <LinkContainer to="/notify"><NavItem eventKey={4} href="#">Notify</NavItem></LinkContainer>
    return (
      <div>
        <Navbar inverse collapseOnSelect>
          <Navbar.Header>
            <Navbar.Brand><Link to="/">Bell security panel</Link></Navbar.Brand>
            <Navbar.Toggle />
          </Navbar.Header>
          <Navbar.Collapse>
            <Nav onSelect={this.onMenuSelect}>
              <LinkContainer to="/recognation"><NavItem eventKey={1}  href="#">Recognation</NavItem></LinkContainer>
              <LinkContainer to="/facesList"><NavItem eventKey={2} href="#">Faces</NavItem></LinkContainer>
              <LinkContainer to="/camerasList"><NavItem eventKey={3} href="#">Cameras</NavItem></LinkContainer>

              <LinkContainer to="/log"><NavItem eventKey={5} href="#">Log</NavItem></LinkContainer>
            </Nav>
            <Nav pullRight>
              <NavItem eventKey={0} onClick={this.doLogin.bind(this)} >{this.state.login}</NavItem> </Nav>
          </Navbar.Collapse>
      </Navbar>
      {this.showContent()}
      </div>
    );
  }
}
