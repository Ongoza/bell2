import React from 'react';
import {Panel, Label, Button, Checkbox, ButtonGroup, Form, Alert, FormControl, FormGroup, Table, Row, Thumbnail,  Col, ControlLabel} from 'react-bootstrap';
import Config from './Config'
import { LinkContainer } from 'react-router-bootstrap'

export default class ListCameras extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      result:"",
      alertTr: false,
      alertType:"info"
    };
  }

  componentDidMount(){
    this.resultTr=false
    this.takeListCameras()
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
        let result =[];
        result = this.tableResult.map((item, i) =>{
          let tbStyle = {textAlign:"center",verticalAlign: "middle"}
            return(
              <tr key={"item_"+i} style={tbStyle}>
                <td style={tbStyle}>{i}</td>
                <td style={tbStyle}>{item["Name"]}</td>
                <td style={tbStyle}>{item["Location"]}</td>
                <td> <Checkbox name={item["IP"]} onChange={this.setVideoChange.bind(this)}></Checkbox></td>
                <td style={tbStyle}><a href="#">
                </a></td>
              </tr>
            )})
        this.resultTr=false;
        return result
      }else{
        return(<div>Wait while connect to cameras </div>)
      }
    }

  handleCameraShow(ev){ev.preventDefault();

  }

  setVideoChange(ev){
    console.log("check",ev.target.checked,ev.target.name)
    // if(ev.target.checked){
    //   console.log("start show video")
    //
    // }else{
    //   console.log("stop show video")
    // }
    const data = new FormData();
    data.append('ip',ev.target.name)
    data.append('active',ev.target.checked)
    fetch('getVideo', {method: 'POST', body: data})
    .then(this.handleErrors)
    .then((response) => {
      response.json().then((body) => {
        console.log("getCamConfig.result",body.name)        
      })
    })
  .catch((err)=>{console.log("Error connect to Server") })
  }

  render(){
    return(
      <div>
        <form>
          <FormGroup inline="true">
            <ControlLabel style={{fontSize: "250%"}}>Cameras&nbsp;&nbsp;</ControlLabel>
            <LinkContainer to="/config"><Button bsStyle="primary" name ="bt" key ="bt" >Config</Button></LinkContainer>
          </FormGroup>
        </form>
        <Table responsive striped bordered condensed>
          <thead>
            <tr style={{textAlign:"center",verticalAlign: "middle"}}>
              <th>#</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Name</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Location</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Active video</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Video</th>
            </tr>
          </thead>
          <tbody>
        {this.showCameras()}
      </tbody>
    </Table>
    </div>
    )
  }
}
