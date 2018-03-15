import React, { Component } from 'react'
import {Navbar, Nav,MenuItem, NavDropdown , NavItem} from 'react-bootstrap'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import {Route, Link } from "react-router-dom"
import { LinkContainer } from 'react-router-bootstrap';

import Camera from './Camera'
import Upload from './Upload'
import ListPhotos from './ListPhotos'
import Recognation from './Recognation'
import StartInfo from './StartInfo'

var counter = 0
var ctx

class App extends Component {
  componentDidMount(){
    console.log("mount comp2")
  }

  onMenuSelect(ev){ //ev.preventDefault()
    console.log("ev=",ev)
  }

  render() {
    //<Camera text="tick=0" ></Camera>
    // <ListPhotos></ListPhotos>
    // <p style={{display: 'flex', justifyContent: 'center'}}><b> Video from web camera.</b></p>
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
              <LinkContainer to="/faceList"><NavItem eventKey={2} href="#">Faces list</NavItem></LinkContainer>
            </Nav>
            <Nav pullRight> <NavItem eventKey={1} href="#">Login</NavItem></Nav>
          </Navbar.Collapse>
      </Navbar>
      <Route exact={true} path="/" component={StartInfo}/>
      <Route path="/recognation" component={Recognation}/>
      <Route path="/faceList" component={ListPhotos}/>
      </div>
    );
  }
}

export default App;
