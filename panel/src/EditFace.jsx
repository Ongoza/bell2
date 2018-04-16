import React, { Component } from 'react';
import {Table, Panel, Tooltip, OverlayTrigger , Label, Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const tooltipDelete =(<Tooltip id="tooltipDelete">Delete</Tooltip>);
const tooltipEdit =(<Tooltip id="tooltipEdit">Edit</Tooltip>);

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
    // let str = this.props.match.params.id.replace(/\.[^/.]+$/, "")
    let name = this.props.match.params.id.split("_")
    if(name[1]==undefined){name[1]=""}
    this.setState({firstName:name[0],secondName:name[1]})
    let str_auth = 'Basic ' + localStorage.getItem('id_token')
    fetch('../getOneFace?'+this.props.match.params.id,{headers: new Headers({'Authorization': str_auth})})
        .then(this.handleErrors)
        .then((response) => {
            let jResponse = response.json()
            console.log("jResponse=",jResponse)
            jResponse.then((body) => {
              this.tableResult = body.getFaceResult
              this.resultTr=true;
              console.log("this.resultTr",this.tableResult)
              this.setState({ resultTr: !this.state.resultTr });
          })
        })
      .catch((err)=>{
        console.log("Error connect to Server")
      })
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
    let str = filename.replace(/\.[^/.]+$/, "")
    console.log("ext=",str)
    let name = str.split("_")
    if(name[1]==undefined){name[1]=""}
    if( this.firstName.value!=name[0] || this.secondName.value!=name[1] ){tr = true}
    if(ifFiles>0){tr = true; data.append('file', this.fileUpload.files[0])}
    if(tr){
        data.append('fileName', firstName+'_'+secondName);
        data.append('filesList', JSON.stringify(this.tableResult));
        data.append('fileOld', this.props.match.params.id);
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

onDelete(e){e.preventDefault();

}
  showPhotos(){
    console.log("start show photos")
    if(this.tableResult){
      return this.tableResult.map((item,i)=>{
        return(
        <FormGroup>
          <Col componentClass={ControlLabel} sm={2}> </Col>
            <Col sm={2}> <img width="128" height="128" src={"../faces/"+item}/> </Col>
            <Col sm={1}>
              <FormControl name ="files" key ="files" label="File"  inputRef={ref => { this.fileUpload = ref; }} type="file" />
              <div style={{marginTop:"10px"}}>

                  <a href="#"><span id={item} className="glyphicon glyphicon-remove" onClick={this.onDelete.bind(this)}><b>Delete</b></span></a>
               </div>
            </Col>
          </FormGroup>)
      })
  }}

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
            <Col componentClass={ControlLabel} sm={2}> Name: </Col>
              <Col sm={5}>
                <FormControl name ="firstName" key ="firstName"  inputRef={ref => { this.firstName = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.firstName} />
              </Col>
                <Col sm={5}>
                <FormControl name ="secondName" key ="secondName"  inputRef={ref => { this.secondName = ref; }} onChange={this.onChange.bind(this)}  type="text" value={this.state.secondName} />
              </Col>
            </FormGroup>
            <FormGroup>
              <Col smOffset={2} sm={10}>
                <ButtonGroup>
                <LinkContainer to="/facesList"><Button bsStyle="primary" name ="btBack" key ="btBack" >Back</Button></LinkContainer>
                <Button bsStyle="primary" onClick={this.handleUpdateFace} name ="btUpdate" key ="bt" >Update</Button>
                </ButtonGroup>
              </Col>
            </FormGroup>
            <FormGroup>
              <Col componentClass={ControlLabel} sm={2}> Photos: </Col>
            </FormGroup>
            {this.showPhotos()}
          </Form>
          {this.showResult()}
        </Panel.Body>
      </Panel>
    </div>)}}
