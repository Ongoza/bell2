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
      fetch('config/notify.json')
      .then(this.handleErrors)
      .then((response) => {
          let jResponse = response.json()
          console.log("jResponse=",jResponse)
          jResponse.then((body) => {
            // this.tableResult = body.geFacesResult
            // this.resultTr=true;
            this.config_body = body
            console.log("this.resultTr",body)

            this.setState({ resultTr: !this.state.resultTr });
        })
      })
    .catch((err)=>{
      console.log("Error connect to Server")
    })
}

  handleUpdateConfig(){

  }

  showForm(){
    if(this.config_body){
      let items = Object.keys(this.config_body).map((key)=>{
        return (
          <FormGroup>
          <Col componentClass={ControlLabel} sm={2}> {key} </Col>
            <Col sm={5}>
              <FormControl name ="files" key ="files" label="File"  inputRef={ref => { this.fileUpload = ref; }} type="text" value={this.config_body[key]} />
            </Col>
          </FormGroup>
        )
      })
      return(
        <div id = "configId" key ="configId" >
          <Form horizontal name ="form" key ="form" >
            {items}
          </Form>
          <Button bsStyle="primary" onClick={this.handleUpdateConfig} name ="bt" key ="bt" >Update</Button>
        </div>
      )
    }
  }

  render() {
    return (
      <div>
        {this.state.resultTr}
        <h3>Notifaction config</h3>
        <div key="config_body" ref="config_body" id="config_body"></div>
        {this.showForm()}
      </div>
    )}
}
