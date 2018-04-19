import React from 'react';
import {Table, Label, Button,Tooltip, OverlayTrigger , ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'

const tooltipDelete =(<Tooltip id="tooltipDelete">Delete</Tooltip>);
const tooltipEdit =(<Tooltip id="tooltipEdit">Edit</Tooltip>);

export default class Alerts extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      result:"",
      alertTr: false,
      alertType:"info",
      Name:"",
      Email:"",
      Phone:"",
      Events:"",
      Type:"",
      Text:""
    }
this.handleAddAlert = this.handleAddAlert.bind(this);
  }

  componentDidMount(){
    this.resultTr=false
    this.takeListAlerts()
  }

  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  handleAddAlert(ev){ ev.preventDefault();
    console.log("Upload config",this.Name)
    let listConfig = [this.Name,this.Email,this.Phone,this.Type,this.Events,this.Text]
    let config = {}
    let tr = ""
    for (let i in listConfig) {
        let name = listConfig[i].name
        if (listConfig[i].value!=""){config[name] = listConfig[i].value
        }else{tr=listConfig[i].name; break}
    }
    if(tr==""){
      console.log("Upload config",config)
      const data = new FormData();
      data.append('body', JSON.stringify(config));
      fetch('../addAlerts/', { method: 'POST', body: data})
      .then(this.handleErrors)
      .then((response) => {
        console.log("server ansver0=",response)
        response.json().then((body) => {
          console.log("server ansver",body)
          this.takeListAlerts()
          // this.setState({ result: body.resultUpload});
          // this.setState({alertType:body.Type})
          // for (let i in listConfig) {listConfig[i].value = ""}
        });
      })
      .catch((err)=>{console.log("Error connect to Server") })
  }else{
    console.log("Please input all info about camera")
    alert("Please fill field: \""+tr+"\"")
  }
  }
  showResult(){
    console.log("alert",this.state.alertTr,this.state.result)
    let result
    if(this.state.result){
      result =  <Alert bsStyle={this.state.alertType} >Result:{this.state.result}</Alert>
      }
    return result
  }



  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  takeListAlerts(){
    let str_auth = 'Basic ' + localStorage.getItem('id_token')
      fetch('getAlerts/',{headers: new Headers({'Authorization': str_auth})})
      .then(this.handleErrors)
      .then((response) => {
        response.json().then((body) => {
          console.log("getAlertsConfig.result",body)
          this.tableResult = body.alerts
          this.resultTr=true;
          console.log("this.resultTr",this.resultTr)
          this.setState({ resultTr: !this.state.resultTr });
        })
      })
    .catch((err)=>{console.log("Error connect to Server") })
  }

  showTable(){
      let result =[];
      console.log("table this.resultTr",this.tableResult)
      if(this.resultTr){
         result = Object.keys(this.tableResult).map((key, i) =>{
          let item = this.tableResult[key]
          console.log("item=",key,item)
          let tbStyle = {textAlign:"center",verticalAlign: "middle"}
        return (
          <tr key={"item_"+i} style={tbStyle}>
            <td style={tbStyle}>{i}</td>
            <td style={tbStyle}>{item["Name"]}</td>
            <td style={tbStyle}>{item["Email"]}</td>
            <td style={tbStyle}>{item["Phone"]}</td>
            <td style={tbStyle}>{item["Type"]}</td>
            <td style={tbStyle}>{item["Events"]}</td>
            <td style={tbStyle}>{item["Text"]}</td>
            <td style={tbStyle}>
              <OverlayTrigger placement="top" overlay={tooltipDelete}>
                <a href="#"><span id={key} className="glyphicon glyphicon-remove" onClick={this.onDelete.bind(this)}></span></a>
              </OverlayTrigger>
              &nbsp;&nbsp;
              <OverlayTrigger placement="top" overlay={tooltipEdit}>
                <LinkContainer to={"/ediAlert/"+key}><a href="#"><span id={key} className="glyphicon glyphicon-edit" ></span></a></LinkContainer>
              </OverlayTrigger>
            </td>
          </tr>)})
      }
      this.resultTr=false;
      return result
    }

  onDelete(e){e.preventDefault();
    if(e.target){
      console.log('e',e.target.id)
      const data = new FormData();
      data.append('body',e.target.id)
      //let data = {"name":'"'+e.target.id+'"'}
      fetch('deleteCamConfig', {
        method: 'POST',
        body: data
      })
      .then((response) => {
        console.log("server  delete ansver0=",response,"==")
        response.json().then((body) => {
          console.log("server delete ansver body=",body)
          console.log("server delete ansver",body.deleteFacesResult)
          this.takeListCameras()
          // let index = this.tableResult.indexOf(body.name)
          // if (index > -1) { this.tableResult.splice(index, 1)}
          // console.log("this.tableResult",this.tableResult)
          //this.tableResult = body.deleteFacesResult
          //`${body.geFacesResult}`
          // this.resultTr=true;
          // this.setState({ resultTr: !this.state.resultTr });
        })
      })
    }
  }
  onChange(e){e.preventDefault();
    this.setState({[e.target.name]:e.target.value})
  }

  render() {
    let tbStyle = {textAlign:"center",verticalAlign: "middle"}

      return (
        <div>
          {this.state.resultTr}
            <Form horizontal name ="form" key ="form" >
              <FormGroup>
              <Col sm={3}><ControlLabel style={{fontSize: "200%"}}>Cameras list</ControlLabel> </Col>
              <Col sm={2}><Button bsStyle="primary" onClick={this.handleAddAlert} name ="bt" key ="bt" >Add new alert</Button></Col>
              </FormGroup>
              <FormGroup>
                <Col sm={12}>
                  <Col componentClass={ControlLabel} sm={1}> User: </Col>
                    <Col sm={3}><FormControl name ="Name" key ="Name"  inputRef={ref => { this.Name = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Name} /> </Col>
                <Col componentClass={ControlLabel} sm={1}> Email: </Col>
                  <Col sm={2}><FormControl name ="Email" key ="Email"  inputRef={ref => { this.Email = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Email} /></Col>
                  <Col componentClass={ControlLabel} sm={1}> Phone: </Col>
                  <Col sm={2}><FormControl name ="Phone" key ="Phone"  inputRef={ref => { this.Phone = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Phone} /></Col>
                </Col><Col sm={12}>
                <Col componentClass={ControlLabel} sm={1}> Type: </Col>
                  <Col sm={2}><FormControl name ="Type" key ="Type"  inputRef={ref => { this.Type = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Type} /></Col>
                    <Col componentClass={ControlLabel} sm={1}> Events: </Col>
                    <Col sm={2}><FormControl name ="Events" key ="Events"  inputRef={ref => { this.Events = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Events} /></Col>
                    <Col componentClass={ControlLabel} sm={1}> Text: </Col>
                    <Col sm={3}><FormControl name ="Text" key ="Text"  inputRef={ref => { this.Text = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Text} /></Col>
                </Col>
              </FormGroup>
            </Form>
            <Table responsive striped bordered condensed>
              <thead>
                <tr style={{textAlign:"center",verticalAlign: "middle"}}>
                  <th>#</th>
                  <th style={tbStyle}>Name</th>
                  <th style={tbStyle}>Email</th>
                  <th style={tbStyle}>Phone</th>
                  <th style={tbStyle}>Type</th>
                  <th style={tbStyle}>Events</th>
                  <th style={tbStyle}>Text</th>
                  <th style={tbStyle}>Action</th>
                </tr>
              </thead>
              <tbody>
                {this.showTable()}
              </tbody>
            </Table>
        </div>
      )}
  }
