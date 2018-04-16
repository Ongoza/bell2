import React from 'react';
import {Panel, Label, Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';

export default class Upload extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
      result:"",
      alertTr: false,
      alertType:"info"
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }
  // componentDidMount() {
  //
  // }
  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  handleUploadImage(ev) {
    ev.preventDefault();
    //const form = ev.target;
    console.log("le2n=",this.secondName.value)
    let firstName = this.firstName.value
    let secondName = this.secondName.value
    let ifFiles = this.fileUpload.files.length
    console.log("size=",this.fileUpload.files[0]);
    if(ifFiles>0){
      if(firstName&&secondName){
        console.log("server send ok")
        const data = new FormData();
        data.append('file', this.fileUpload.files[0]);
        data.append('fileName', firstName+'_'+secondName);
        fetch('upload', {
          method: 'POST',
          body: data,
        })
        .then(this.handleErrors)
        .then((response) => {
          console.log("server ansver0=",response)
          response.json().then((body) => {
            console.log("server ansver",body)
            window.location.reload()
            // this.setState({ result: body.resultUpload});
            // this.setState({alertType:body.Type})
            // this.fileUpload.files = null
            // this.fileUpload.value =""
            // this.firstName.value =""
            // this.secondName.value=""
          });
        })
        .catch((err)=>{console.log("Error connect to Server") })
      }else{console.log("no names")
      this.setState({alertType:"danger"})
      this.setState({result:"Please type name"})
    }}else{console.log("no files for send")
    this.setState({alertType:"danger"})
    this.setState({result:"Please attach file"})
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

  render() {
    return (
      <div>
      <Panel bsStyle="info">
        <Panel.Heading>
          <Panel.Title componentClass="h3">Create new person for recognation</Panel.Title>
        </Panel.Heading>
      <Panel.Body>
          <Form horizontal name ="form" key ="form" >
            <FormGroup>
              <Col componentClass={ControlLabel} sm={2}> Select a photo file </Col>
              <Col sm={10}>
                <FormControl name ="files" key ="files" inputRef={ref => { this.fileUpload = ref; }} type="file" />
              </Col>
            </FormGroup>
            <FormGroup>
            <Col componentClass={ControlLabel} sm={2}> Type the name of people on the photo </Col>
              <Col sm={5}>
                <FormControl name ="firstName" key ="firstName"  inputRef={ref => { this.firstName = ref; }}  type="text" placeholder="First name" />
              </Col>
                <Col sm={5}>
                <FormControl name ="secondName" key ="secondName"  inputRef={ref => { this.secondName = ref; }}  type="text" placeholder="Second name" />
              </Col>
            </FormGroup>
            <FormGroup>
              <Col smOffset={2} sm={10}>
                <Button bsStyle="primary" onClick={this.handleUploadImage} name ="bt" key ="bt" >Upload</Button>
              </Col>
            </FormGroup>
          </Form>
          {this.showResult()}
        </Panel.Body>
      </Panel>
    </div>)}}
