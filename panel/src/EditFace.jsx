import React, { Component } from 'react';
import {Table, Panel, Label, Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';

export default class EditFace extends Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
      result:"",
      firstName:"",
      secondName:"",
      alertTr: false,
      alertType:"info"
    };

    this.handleUpdateFace = this.handleUpdateFace.bind(this);
  }
  componentDidMount() {
    let str = this.props.match.params.id.replace(/\.[^/.]+$/, "")
    let name = str.split("_")
    if(name[1]==undefined){name[1]=""}
    this.setState({firstName:name[0],secondName:name[1]})
  }
  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  handleUpdateFace(ev) {
    ev.preventDefault();
    //const form = ev.target;
    console.log("le2n=",this.firstName.value,this.state.firstName,this.secondName.value,this.state.secondName)
    let firstName = this.firstName.value
    let secondName = this.secondName.value
    let ifFiles = this.fileUpload.files.length
    let data = new FormData();
    let tr = false;
    let filename = this.props.match.params.id;
    let ext = filename.substring(filename.lastIndexOf('.'), filename.length) || filename;
    let str = filename.replace(/\.[^/.]+$/, "")
    console.log("ext=",ext,str)
    let name = str.split("_")
    if(name[1]==undefined){name[1]=""}
    if( this.firstName.value!=name[0] || this.secondName.value!=name[1] ){tr = true}
    if(ifFiles>0){tr = true; data.append('file', this.fileUpload.files[0])}
    if(tr){
        data.append('fileName', firstName+'_'+secondName);
        data.append('fileExt', ext);
        data.append('fileOld', str);
        fetch('../updateFace', {
          method: 'POST',
          body: data,
        })
        .then(this.handleErrors)
        .then((response) => {
          console.log("server ansver0=",response)
          response.json().then((body) => {
            console.log("server ansver",body)
            this.setState({ result: body.resultUpdate});
            this.setState({alertType:body.Type})
          });
        })
        .catch((err)=>{console.log("Error connect to Server") })
      }else{console.log("no changes")
    this.setState({alertType:"info"})
    this.setState({result:"No data changes"})
  }
  }
  onChange(e){e.preventDefault(); this.setState({[e.target.name]:e.target.value})}
  showResult(){
  console.log("alert",this.state.alertTr,this.state.result)
  let result
  if(this.state.result){
    result =  <Alert bsStyle={this.state.alertType} >Result:{this.state.result}</Alert>
    }
  return result
  }

  render() {
    let src = "../faces/"+this.props.match.params.id
    return (
      <div>
      <Panel bsStyle="info">
        <Panel.Heading>
          <Panel.Title componentClass="h3">Edit information about person</Panel.Title>
        </Panel.Heading>
      <Panel.Body>
          <Form horizontal name ="form" key ="form" >
            <FormGroup>
            <Col componentClass={ControlLabel} sm={2}> Update photo: </Col>
              <Col sm={3}> <img width="128" height="128" src={src}/> </Col>
              <Col sm={5}>
                <FormControl name ="files" key ="files" label="File"  inputRef={ref => { this.fileUpload = ref; }} type="file" />
              </Col>
            </FormGroup>
            <FormGroup>
            <Col componentClass={ControlLabel} sm={2}> Name: </Col>
              <Col sm={5}>
                <FormControl name ="firstName" key ="firstName"  inputRef={ref => { this.firstName = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.firstName} />
              </Col>
                <Col sm={5}>
                <FormControl name ="secondName" key ="secondName"  inputRef={ref => { this.secondName = ref; }}  type="text" value={this.state.secondName} />
              </Col>
            </FormGroup>
            <FormGroup>
              <Col smOffset={2} sm={10}>
                <Button bsStyle="primary" onClick={this.handleUpdateFace} name ="bt" key ="bt" >Update</Button>
              </Col>
            </FormGroup>
          </Form>
          {this.showResult()}
        </Panel.Body>
      </Panel>
    </div>)}}
