import React, { Component } from 'react';
import {Table, Panel, Tooltip, OverlayTrigger , Label, Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const tooltipDelete =(<Tooltip id="tooltipDelete">Delete</Tooltip>);
const tooltipEdit =(<Tooltip id="tooltipEdit">Edit</Tooltip>);

export default class EditCamera extends Component {
  constructor(props) {super(props)
    this.state = {
      result:"",
      alertTr: false,
      alertType:"info",
      IP:"0",
      Name:"0",
      Port:"0",
      Recognation:"0",
      Resolution:"0",
      Location:"0"
    }
  }

  componentDidMount() {
    // let str = this.props.match.params.id.replace(/\.[^/.]+$/, "")
    let name = this.props.match.params.id.split("_")
    if(name[1]==undefined){name[1]=""}
    this.setState({firstName:name[0],secondName:name[1]})
    let str_auth = 'Basic ' + localStorage.getItem('id_token')
      fetch('getCamConfig/',{headers: new Headers({'Authorization': str_auth})})
    .then(this.handleErrors)
    .then((response) => {
      response.json().then((body) => {
        console.log("getCamConfig.result",body.cameras,this.props.match.params.id)
        this.tableResult = body.cameras
        this.item = body.cameras[this.props.match.params.id]
        console.log("getCamConfig.result IP=",this.item["IP"])
        let IP = this.item["IP"]
        let Port = this.item["Port"]
        let Name = this.item["Name"]
        let Recognation = this.item["Recognation"]
        let Resolution = this.item["Resolution"]
        let Location = this.item["Location"]
        this.setState({ IP: IP });
        this.setState({ Port: Port});
        this.setState({ Name: Name});
        this.setState({ Recognation: Recognation});
        this.setState({ Resolution: Resolution});
        this.setState({ Location: Location});
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

  handleUpdateCamera(ev) {
    ev.preventDefault();
    //const form = ev.target;
    console.log("le2n=",this.state.IP)
    let id = this.props.match.params.id
    let dataJson ={}
    dataJson[id]={
      "IP":this.IP.value,
      "Port":this.Port.value,
      "Location":this.Location.value,
      "Recognation": this.Recognation.value,
      "Resolution": this.Resolution.value}
      console.log("json=",dataJson)
    let data = new FormData();
        data.append('body',JSON.stringify(dataJson));
        data.append('id',id);
        fetch('../updateCamera/', {
          method: 'POST',
          body: data
        })
        .then(this.handleErrors)
        .then((response) => {
          console.log("server ansver0=",response)
          response.json().then((body) => {
            console.log("server ansver",body)
            this.setState({ result: body.updateCameraResult});
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
    let src = "../faces/"+this.props.match.params.id
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
                    <Button bsStyle="primary" onClick={this.handleUpdateCamera.bind(this)} name ="btUpdate" key ="bt" >Update</Button>
                  </ButtonGroup>
              </Col></Col>
            </FormGroup>
            <FormGroup>
              <Col sm={12}>
                <Col componentClass={ControlLabel} sm={1}> IP: </Col>
                  <Col sm={3}><FormControl name ="IP" key ="IP"  inputRef={ref => { this.IP = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.IP} />
                  </Col>
              <Col componentClass={ControlLabel} sm={1}> Port: </Col>
                <Col sm={2}><FormControl name ="Port" key ="Port"  inputRef={ref => { this.Port = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Port} /></Col>
              </Col>
            </FormGroup>
            <FormGroup>
              <Col sm={12}>
                <Col componentClass={ControlLabel} sm={1}> Name: </Col>
                <Col sm={2}><FormControl name ="Name" key ="Name"  inputRef={ref => { this.Name = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Name} /></Col>
                <Col componentClass={ControlLabel} sm={1}> Recognation: </Col>
                <Col sm={2}><FormControl name ="Recognation" key ="Recognation"  inputRef={ref => { this.Recognation = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Recognation} /></Col>
                <Col componentClass={ControlLabel} sm={1}> Resolution: </Col>
                <Col sm={2}><FormControl name ="Resolution" key ="Resolution"  inputRef={ref => { this.Resolution = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Resolution} /></Col>
                <Col componentClass={ControlLabel} sm={1}> Location: </Col>
                <Col sm={2}><FormControl name ="Location" key ="Location"  inputRef={ref => { this.Location = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.Location} /></Col>
              </Col>
            </FormGroup>
          </Form>
          {this.showResult()}
        </Panel.Body>
      </Panel>
    </div>)}}
