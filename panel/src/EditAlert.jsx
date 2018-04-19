import React, { Component } from 'react';
import {Table, Panel, Tooltip, OverlayTrigger , Label, Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const tooltipDelete =(<Tooltip id="tooltipDelete">Delete</Tooltip>);
const tooltipEdit =(<Tooltip id="tooltipEdit">Edit</Tooltip>);

export default class EditAlert extends Component {
  constructor(props) {super(props)
    this.state = {
      result:"",
      alertTr: false,
      alertType:"info",
      Name:"0",
      Email:"0",
      Phone:"0",
      Events:"0",
      Type:"0",
      Text:"0"
    }
  }

  componentDidMount() {
    // let str = this.props.match.params.id.replace(/\.[^/.]+$/, "")
    console.log("getAlerts.id==")
    let name = this.props.match.params.id.split("_")
    if(name[1]==undefined){name[1]=""}
    this.setState({firstName:name[0],secondName:name[1]})
    let str_auth = 'Basic ' + localStorage.getItem('id_token')
      fetch('getAlerts/',{headers: new Headers({'Authorization': str_auth})})
    .then(this.handleErrors)
    .then((response) => {
      response.json().then((body) => {
        console.log("getAlerts.result==",body)
        console.log("getAlerts.result==",body,this.props.match.params.id)
        this.tableResult = body.alerts
        this.item = body.alerts[this.props.match.params.id]
        console.log("getAlerts.result Name=",this.item["Name"])
        let Name = this.item["Name"]
        let Email = this.item["Email"]
        let Phone = this.item["Phone"]
        let Type = this.item["Type"]
        let Text = this.item["Text"]
        let Events = this.item["Events"]
        this.setState({ Name: Name });
        this.setState({ Phone: Phone});
        this.setState({ Email: Email});
        this.setState({ Type: Type});
        this.setState({ Text: Text});
        this.setState({ Events: Events});
        this.resultTr=true;
        console.log("this.resultTr",this.resultTr)
        this.setState({ resultTr: !this.state.resultTr });
      })
    })
  .catch((err)=>{console.log("Error connect to Server") })
  }

  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  handleUpdateAlert(ev) {
    ev.preventDefault();
    //const form = ev.target;
    console.log("le2n=",this.state.Name)
    let id = this.props.match.params.id
    let dataJson ={}
    dataJson[id]={
      "Name":this.name.value,
      "Email":this.Email.value,
      "Phone":this.Phone.value,
      "Type": this.Type.value,
      "Events": this.Events.value,
      "Text": this.Text.value
    }
      console.log("json=",dataJson)
    let data = new FormData();
        data.append('body',JSON.stringify(dataJson));
        data.append('id',id);
        fetch('../updateAlerts/', {
          method: 'POST',
          body: data
        })
        .then(this.handleErrors)
        .then((response) => {
          console.log("server ansver0=",response)
          response.json().then((body) => {
            console.log("server ansver",body)
            this.setState({ result: body.updateAlertsResult});
            this.setState({alertType:body.Type})
          });
        })
        .catch((err)=>{console.log("Error connect to Server") })
    this.setState({alertType:"info"})
    this.setState({result:"No data changes"})
  }

  onChange(e){e.preventDefault();
    this.setState({[e.target.name]:e.target.value})
  }

  showResult(){
  console.log("alert",this.state.alertTr,this.state.result)
  let result
  if(this.state.result){
    result =  <Alert bsStyle={this.state.alertType} >Result:{this.state.result}</Alert>
    }
  return result
  }

onDelete(e){e.preventDefault();

}

  render() {
    // let src = "../faces/"+this.props.match.params.id
    console.log("Alerts!!!!!!")
    return (
      <div>
      <Panel bsStyle="info">
        <Panel.Heading>
          <Panel.Title componentClass="h3">Edit camera information </Panel.Title>
        </Panel.Heading>
      <Panel.Body>
          <Form horizontal name ="form" key ="form" >
            <FormGroup>
              <Col sm={12}>
                <Col componentClass={ControlLabel} sm={1}> Camera </Col>
                <Col sm={8}>
                  <ButtonGroup>
                    <LinkContainer to="/config"><Button bsStyle="primary" name ="btBack" key ="btBack" >Back</Button></LinkContainer>
                    <Button bsStyle="primary" onClick={this.handleUpdateAlert.bind(this)} name ="btUpdate" key ="bt" >Update</Button>
                  </ButtonGroup>
              </Col></Col>
            </FormGroup>
            <FormGroup>
              <Col sm={12}>
                <Col componentClass={ControlLabel} sm={1}> Name: </Col>
                  <Col sm={3}><FormControl name ="Name" key ="Name"  inputRef={ref => { this.Name = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.IP} />
                  </Col>
              <Col componentClass={ControlLabel} sm={1}> Email: </Col>
                <Col sm={2}><FormControl name ="Email" key ="Email"  inputRef={ref => { this.Email = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Port} /></Col>
                <Col componentClass={ControlLabel} sm={1}> Phone: </Col>
                <Col sm={2}><FormControl name ="Phone" key ="Phone"  inputRef={ref => { this.Phone = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Resolution} /></Col>
                <Col componentClass={ControlLabel} sm={1}> Type: </Col>
                <Col sm={2}><FormControl name ="Type" key ="Type"  inputRef={ref => { this.Type = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Location} /></Col>
                  <Col componentClass={ControlLabel} sm={1}> Events: </Col>
                  <Col sm={2}><FormControl name ="Events" key ="Events"  inputRef={ref => { this.Events = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Name} /></Col>
                  <Col componentClass={ControlLabel} sm={1}> Text: </Col>
                  <Col sm={2}><FormControl name ="Text" key ="Text"  inputRef={ref => { this.Text = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Recognation} /></Col>

              </Col>
            </FormGroup>
          </Form>
          {this.showResult()}
        </Panel.Body>
      </Panel>
    </div>)}}
