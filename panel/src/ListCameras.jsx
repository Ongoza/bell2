import React from 'react';
import {Panel, Label, Button, Checkbox, ButtonGroup, Form, Alert, FormControl, FormGroup, Table, Row, Thumbnail,  Col, ControlLabel} from 'react-bootstrap';
import Config from './Config'
import { LinkContainer } from 'react-router-bootstrap'

const CheckVideo = props => ( <div className={props.className}/>)

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

  // <Checkbox checked="" name={item["IP"]} key="stream_0_ch" onChange={this.handleCameraShow.bind(this)}></Checkbox>
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
                <td style={tbStyle}>
                  <a href="#"><span id={item["IP"]} name={item["IP"]} className="glyphicon glyphicon-ban-circle" onClick={this.CameraStreaming.bind(this)}></span></a>
                </td>
                <td style={tbStyle}>
                    <img id={"stream_0"} ref={"stream_0"} width="128" height="128" src="#"  />
              </td>
              </tr>
            )})
        this.resultTr=false;
        return result
      }else{
        return(<tr><td colSpan="4">Wait while connect to cameras </td></tr>)
      }
    }

  CameraStreaming(ev){ ev.preventDefault();
    console.log("show camera",ev.target)
    if(ev.target.className=="glyphicon glyphicon-ban-circle"){
      ev.target.className="glyphicon glyphicon-ok-circle"
      console.log("start show camera")
      this.refs.stream_0.src = "http://localhost:3000/stream"
    }else{
      ev.target.className="glyphicon glyphicon-ban-circle"
      this.refs.stream_0.src = "#"}
      this.resultTr=true;
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
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Streaming</th>
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
