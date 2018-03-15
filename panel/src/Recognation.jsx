import React from 'react';
import {Table, Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';

export default class Recognation extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      imageURL: '',
      result:"",
      alertType:"info",
      loading: true
    };
    this.handleUploadImage = this.handleUploadImage.bind(this)
    this.imgUrl = false
    this.resultTr = false
    // this.fileUpload = {"files": null, "value" :""}
  }

  onReloadClick(ev){
    ev.preventDefault()
    window.location.reload()
  }
  
  handleUploadImage(ev){ ev.preventDefault()
    let ifFiles = this.fileUpload.files.length
    if(ifFiles>0){
      console.log("size=",this.fileUpload.files[0].size)
      if(this.fileUpload.files[0].size<3000000){
        console.log("server send ok")
        const data = new FormData()
        this.setState({ loading: false})
        data.append('file', this.fileUpload.files[0])
        fetch('uploadRecognation', {
          method: 'POST',
          body: data,
        }).then((response) => {
          console.log("server ansver0=",response)
          response.json().then((body) => {
            console.log("server ansver",body)
            if(body.Type=='info'){
              this.resultTr = true
              this.imgUrl= body.uploadRecognation
              console.log("this.imgUrl",this.imgUrl,this.resultTr)
            }else{
              this.setState({alertType:body.Type})
              if(this.fileUpload){
                this.fileUpload.files = null
                this.fileUpload.value =""
              }
            }
            this.setState({ loading: true});
            this.setState({ result: body.uploadRecognation})
          });
        });
      }else{
      console.log("files bigger then 2MB")
      this.setState({alertType:"danger"})
      this.setState({result:"Please select file with size less than 2MB"})
      }}else{console.log("no files for send")
    this.setState({alertType:"danger"})
    this.setState({result:"Please attach file"})
  }
  }

  componentDidMount() { this.resultTr=false}

  handleChange(ev){ ev.preventDefault();  this.setState({result:""})}

  showPage(){
    console.log("showPage=",this.resultTr,"-",this.imgUrl)
    if(!this.state.loading){return (<div style={{textAlign:"center"}}><img style={{height:"60%",width:"60%"}} src="img/tenor.gif"/></div>)
    }else{
      if (!this.resultTr){
      return(
        <Form horizontal name ="form" key ="form" >
          <FormGroup>
            <Col componentClass={ControlLabel} sm={3}> Select a photo for recognation</Col>
            <Col sm={8}>
              <FormControl name ="files" key ="files" inputRef={ref => { this.fileUpload = ref}} type="file" onChange={this.handleChange.bind(this)} />
            </Col>
          </FormGroup>
          <FormGroup>
            <Col smOffset={1} sm={3}>
              <Button bsStyle="primary" onClick={this.handleUploadImage} name ="bt" key ="bt" >Upload</Button>
            </Col>
          </FormGroup>
        </Form>)
    }else {
          return( <div style={{textAlign:"center"}}>
            <Button bsStyle="primary" onClick={this.onReloadClick}>Try new</Button>
            <h2>Result</h2>
            <img style={{height:"100%",width:"100%"}} src={this.imgUrl}/>
          </div>)
         }
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
        <h1>Recognation</h1>
        {this.showPage()}
          {this.showResult()}
      </div>)}
}
