import React from 'react';
import {Table, Panel, Tooltip, OverlayTrigger , Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'

const tooltipDelete =(<Tooltip id="tooltipDelete">Delete</Tooltip>);
const tooltipEdit =(<Tooltip id="tooltipEdit">Edit</Tooltip>);

export default class Notify extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
      result:"",
      resultTr: false,
      alertType:"info"
    };

  }
  componentDidMount() {
    this.resultTr=false;
    this.takeTableData()
  }

  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  takeTableData(){
      fetch('notify/notify.cfg')
      .then(this.handleErrors)
      .then((response) => {
          let jResponse = response.json()
          console.log("jResponse=",jResponse)
          jResponse.then((body) => {
            // this.tableResult = body.geFacesResult
            // this.resultTr=true;
            console.log("this.resultTr",body)
            this.refs.config_body.innerHTML = body
            this.setState({ resultTr: !this.state.resultTr });
        })
      })
    .catch((err)=>{
      console.log("Error connect to Server")
    })
}



  render() {
    return (
      <div>
        {this.state.resultTr}
        <h3>Notifaction config</h3>
        <div key="config_body" ref="config_body" id="config_body"></div>
      </div>
    )}
}
