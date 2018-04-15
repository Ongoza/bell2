import React from 'react';
import {Table, Nav, Pager, NavItem, Panel, Tooltip, OverlayTrigger , Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';

import createBrowserHistory from "history/createBrowserHistory"

const history = createBrowserHistory({
  forceRefresh: true
})

export default class Login extends React.Component {
  constructor() {
    super()
    this.state = { resultTr: false}
  }

  handleSubmit(ev) {ev.preventDefault();
    console.log("click",this.login.value)
    fetch('login/?id=demo&pass=demo')
    .then(this.handleErrors)
    .then((response) => {
      response.json().then((body) => {
        console.log("getCamConfig.result",body)
        localStorage.setItem('id_token', body.key)
        // this.resultTr=true;
        // console.log("this.resultTr",this.resultTr)
        // this.setState({ resultTr: !this.state.resultTr });
        history.push("/")

      })
    })
  .catch((err)=>{console.log("Error connect to Server") })
  }

  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  render() {
    const {errorMessage} = this.props

    return (
        <Form inline>
          {this.state.resultTr}
            <FormGroup controlId="formHorizontalEmail">
                <ControlLabel>Email </ControlLabel>
                <FormControl type="username" inputRef={ref => { this.login = ref; }} onChange={this.handleChange} placeholder="Name" />
            </FormGroup>
            <FormGroup controlId="formHorizontalPassword">
                <ControlLabel>Password </ControlLabel>
                <FormControl type="password" inputRef={ref => { this.pass = ref; }} onChange={this.handleChange} placeholder="Password" />
            </FormGroup>
            <Button onClick={(event) => this.handleSubmit(event)}>Login</Button>
            {errorMessage &&
            <p style={{color:'red'}}>{errorMessage}</p>
            }
        </Form>
    )
  }
}
