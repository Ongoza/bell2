import React from 'react';
import {Table, Panel, Tooltip, OverlayTrigger , Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import Upload from './Upload'
import { LinkContainer } from 'react-router-bootstrap'

const tooltipDelete =(<Tooltip id="tooltipDelete">Delete</Tooltip>);
const tooltipEdit =(<Tooltip id="tooltipEdit">Edit</Tooltip>);

export default class ListPhotos extends React.Component {
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
    if(str_auth){
    fetch('getFaces/',{headers: new Headers({'Authorization': str_auth})})
      .then(this.handleErrors)
      .then((response) => {
          // console.log("response=",response.text())
          let jResponse = response.json()
          console.log("jResponse=",jResponse)
          jResponse.then((body) => {
            // console.log("this.body",body.getFacesResult)
            this.tableResult = body.getFacesResult
            this.resultTr=true;
            // console.log("this.resultTr",this.tableResult)
            this.setState({ resultTr: !this.state.resultTr });
        })
      })
    .catch((err)=>{
      console.log("Error connect to Server")
    })
  }else{
    console.log("Please login")
  }
}

  showTable(){
    let result =[];
    console.log("this.resultTr",this.resultTr)
    if(this.resultTr){
      result = Object.keys(this.tableResult).map((key, i) =>{
        let src = "faces/"+this.tableResult[key][0]
        let tbStyle = {textAlign:"center",verticalAlign: "middle"}
        // let strName = key.replace(/\.[^/.]+$/, "")
        let strNames = key.replace('_'," ") + "  ("+this.tableResult[key].length+" photos)"
      return (
        <tr key={"item_"+key} style={tbStyle}>
          <td>{i}</td>
          <td style={tbStyle}>{strNames}</td>
          <td style={tbStyle}><img width="128" height="128" src={src}/></td>
          <td style={tbStyle}>
            <OverlayTrigger placement="top" overlay={tooltipDelete}>
              <a href="#"><span id={key} className="glyphicon glyphicon-remove" onClick={this.onDelete.bind(this)}></span></a>
             </OverlayTrigger>
            &nbsp;&nbsp;
            <OverlayTrigger placement="top" overlay={tooltipEdit}>
              <LinkContainer to={"/editFace/"+key}><a href="#"><span id={key} className="glyphicon glyphicon-edit" ></span></a></LinkContainer>
            </OverlayTrigger>
          </td>
        </tr>)})
    }
    this.resultTr=false;
    return result
  }

onDelete(e){e.preventDefault();
  if(e.target){
    console.log('e',e.target.id)
    const data = new FormData();
    data.append('name',e.target.id)
    //let data = {"name":'"'+e.target.id+'"'}
    fetch('deleteFace', {
      method: 'POST',
      body: data
    })
    .then((response) => {
      console.log("server  delete ansver0=",response,"==")
      response.json().then((body) => {
        console.log("server delete ansver body=",body)
        console.log("server delete ansver",body.deleteFacesResult)
        this.takeTableData()
        // let index = this.tableResult.indexOf(body.name)
        //
        // if (index > -1) { this.tableResult.splice(index, 1)}
        // console.log("this.tableResult",this.tableResult)
        // //this.tableResult = body.deleteFacesResult
        // //`${body.geFacesResult}`
        // this.resultTr=true;
        // this.setState({ resultTr: !this.state.resultTr });
      })
    })
  }
}
  render() {
    return (
      <div>
        {this.state.resultTr}
        <Upload></Upload>
        <h3>List of people for recognation</h3>
        <Table responsive striped bordered condensed>
          <thead>
            <tr style={{textAlign:"center",verticalAlign: "middle"}}>
              <th>#</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Name</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Photo</th>
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {this.showTable()}
          </tbody>
        </Table>
      </div>
    )}
}
