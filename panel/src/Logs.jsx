import React from 'react';
import {Table, Panel, Tooltip, OverlayTrigger , Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
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
      fetch('../log/server.log')
      .then(this.handleErrors)
      .then((response) => {
        console.log("server ansver0=",response)
        response.text().then((body) => {
          this.log_text = body.replace(/(?:\r\n|\r|\n)/g, '<br />');
          this.refs.log_body.innerHTML = this.log_text
          // console.log("server ansver2",this.log_text);
          this.setState({ resultTr: !this.state.resultTr});
          // this.setState({alertType:body.Type})
        });
      })
      .catch((err)=>{console.log("Error connect to Server") })
}
  clearLog(){
    fetch('../clearLog')
    .then(this.handleErrors)
    .then((response) => {
      console.log("server ansver0=",response)
      this.takeTableData();
    })
    .catch((err)=>{console.log("Error connect to Server") })
  }

  render() {
    return (
      <div>
        {this.state.resultTr}
        <h3>Logs</h3>
        <Button bsStyle="primary" onClick={this.clearLog} name ="btUpdate" key ="bt" >Clear log</Button>
        <div key="log_body" ref="log_body" id="log_body"></div>
      </div>
    )}
}
