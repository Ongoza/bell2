import React from 'react';
import {Table, Label, Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';

export default class Config extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      result:"",
      alertTr: false,
      alertType:"info"
    }
      this.handleAddCamera = this.handleAddCamera.bind(this);
  }

  componentDidMount(){
    this.resultTr=false
    this.takeListCameras()
  }

  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  handleAddCamera(ev){ ev.preventDefault();
    console.log("Upload config")
    let listConfig = [this.Name,this.IP,this.Resolution,this.Location]
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
      fetch('addCamConfig', { method: 'POST', body: data})
      .then(this.handleErrors)
      .then((response) => {
        console.log("server ansver0=",response)
        response.json().then((body) => {
          console.log("server ansver",body)
          this.setState({ result: body.resultUpload});
          this.setState({alertType:body.Type})
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

  takeListCameras(){
      fetch('getCamConfig')
      .then(this.handleErrors)
      .then((response) => {
        response.json().then((body) => {
          console.log("getCamConfig.result",body.cameras)
          this.tableResult = body.cameras
          this.resultTr=true;
          console.log("this.resultTr",this.resultTr)
          this.setState({ resultTr: !this.state.resultTr });
        })
      })
    .catch((err)=>{console.log("Error connect to Server") })
  }

  showCameras(){
      if(this.resultTr){
        return(<div>Ok connect to cameras </div>)
      }else{
        return(<div>Wait while connect to cameras </div>)
      }
    }

    showTable(){
      let result =[];
      console.log("this.resultTr",this.resultTr)
      if(this.resultTr){
        result = this.tableResult.map((item, i) =>{
          let tbStyle = {textAlign:"center",verticalAlign: "middle"}
        return (
          <tr key={"item_"+i} style={tbStyle}>
            <td style={tbStyle}>{i}</td>
            <td style={tbStyle}>{item["Name"]}</td>
            <td style={tbStyle}>{item["IP"]}</td>
            <td style={tbStyle}>{item["Resolution"]}</td>
            <td style={tbStyle}>{item["Location"]}</td>
            <td style={tbStyle}><a href="#"><span id={item} className="glyphicon glyphicon-remove" onClick={this.onDelete.bind(this)}></span></a></td>
          </tr>)})
      }
      this.resultTr=false;
      return result
    }

  onDelete(e){e.preventDefault();
    if(e.target){
      console.log('e',e.target.id)
      const data = new FormData();
      data.append('camera',e.target.id)
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
          let index = this.tableResult.indexOf(body.name)
          if (index > -1) { this.tableResult.splice(index, 1)}
          console.log("this.tableResult",this.tableResult)
          //this.tableResult = body.deleteFacesResult
          //`${body.geFacesResult}`
          this.resultTr=true;
          this.setState({ resultTr: !this.state.resultTr });
        })
      })
    }
  }

  render() {
    let tbStyle = {textAlign:"center",verticalAlign: "middle"}
      return (
        <div>
          {this.state.resultTr}

          <h3>Cameras list</h3>
            <Form horizontal name ="form" key ="form" >
              <FormGroup>
              <Col sm={2}><Button bsStyle="primary" onClick={this.handleAddCamera} name ="bt" key ="bt" >Add camera</Button></Col>
                <Col sm={2}><FormControl name ="Name" key ="Name"  inputRef={ref => { this.Name = ref; }}  type="text" placeholder="Name" /></Col>
                <Col sm={2}><FormControl name ="IP" key ="IP"  inputRef={ref => { this.IP = ref; }}  type="text" placeholder="IP" /></Col>
                <Col sm={2}><FormControl name ="Resolution" key ="Resolution"  inputRef={ref => { this.Resolution = ref; }}  type="text" placeholder="Resolution" /></Col>
                <Col sm={3}><FormControl name ="Location" key ="Location"  inputRef={ref => { this.Location = ref; }}  type="text" placeholder="Location" /></Col>

              </FormGroup>
            </Form>
          <Table responsive striped bordered condensed>
            <thead>
              <tr style={{textAlign:"center",verticalAlign: "middle"}}>
                <th>#</th>
                <th style={tbStyle}>Name</th>
                <th style={tbStyle}>IP</th>
                <th style={tbStyle}>Resolution</th>
                <th style={tbStyle}>Location</th>
                <th style={tbStyle}>Delete</th>
              </tr>
            </thead>
            <tbody>
              {this.showTable()}
            </tbody>
          </Table>
        </div>
      )}
  }
