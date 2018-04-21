import React from 'react';
import {Table, Panel, Tooltip, OverlayTrigger , Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'

const tooltipDelete =(<Tooltip id="tooltipDelete">Delete</Tooltip>);
const tooltipEdit =(<Tooltip id="tooltipEdit">Edit</Tooltip>);

export default class Notify extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
      result:"",
      resultTr: false,
      alertType:"info"
    };

  }
  componentDidMount() {
    this.resultTr=false;
    this.takeTableData()
  }

  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  takeTableData(){
    let str_auth = 'Basic ' + localStorage.getItem('id_token')
    fetch('getAlerts/',{headers: new Headers({'Authorization': str_auth})})
      // fetch('../config/alerts.json')
      .then(this.handleErrors)
      .then((response) => {
        // console.log("Response=",response)
          let jResponse = response.json()
          // console.log("jResponse=",jResponse)
          jResponse.then((body) => {
            console.log("body",body)
            this.tableResult = body.alerts
            this.resultTr=true;
            this.setState({ resultTr: !this.state.resultTr });
            // this.config_body = body


            this.setState({ resultTr: !this.state.resultTr });
        })
      })
    .catch((err)=>{
      console.log("Error connect to Server")
    })
}

  handleUpdateConfig(){

  }

    showAlerts(){
       if(this.resultTr){
         let result =[];
         // console.log("0 table=",this.tableResult)
         result = Object.keys(this.tableResult).map((key, i) =>{
           let item = this.tableResult[key]
           let tbStyle = {textAlign:"center",verticalAlign: "middle"}
             return(
               <tr key={"item_"+i} style={tbStyle}>
                 <td style={tbStyle}>{i}</td>
                 <td style={tbStyle}>{item['Name']}</td>
                 <td style={tbStyle}>{item["Email"]}</td>
                 <td style={tbStyle}>{item["Phone"]}</td>
                 <td style={tbStyle}>{item["Type"]}</td>
                 <td style={tbStyle}>{item["Events"]}</td>
                 <td style={tbStyle}>{item["Text"]}</td>
               </tr>
             )})
        // this.resultTr=false;
        return result
      }else{
        return(<tr><td colSpan="7">Wait while connect to server</td></tr>)
      }
    }

  render() {
    return (
      <div>
        <form>
          <FormGroup inline="true">
            <ControlLabel style={{fontSize: "250%"}}>Alerts&nbsp;&nbsp;</ControlLabel>
            <LinkContainer to="/alerts/"><Button bsStyle="primary" name ="bt" key ="bt" >Edit Alerts</Button></LinkContainer>
          </FormGroup>
        </form>
        <Table responsive striped bordered condensed>
          <thead>
            <tr style={{textAlign:"center",verticalAlign: "middle"}}>
              <th>#</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>User name</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Email</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Phone</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Type</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Events</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Text</th>
            </tr>
          </thead>
          <tbody>
        {this.showAlerts()}
      </tbody>
    </Table>
    </div>
    )}
}
