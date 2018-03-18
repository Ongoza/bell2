import React from 'react';
import {Table, Panel, Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import Upload from './Upload'

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
      fetch('getFaces')
      .then(this.handleErrors)
      .then((response) => {
          let jResponse = response.json()
          console.log("jResponse=",jResponse)
          jResponse.then((body) => {
            this.tableResult = body.geFacesResult
            this.resultTr=true;
            console.log("this.resultTr",this.resultTr)
            this.setState({ resultTr: !this.state.resultTr });
        })
      })
    .catch((err)=>{
      console.log("Error connect to Server")
    })
}

  showTable(){
    let result =[];
    console.log("this.resultTr",this.resultTr)
    if(this.resultTr){
      result = this.tableResult.map((item, i) =>{
        let src = "faces/"+item
        let tbStyle = {textAlign:"center",verticalAlign: "middle"}
        let strName = item.replace(/\.[^/.]+$/, "")
        let arrNames = strName.replace('_'," ")
      return (
        <tr key={"item_"+i} style={tbStyle}>
          <td>{i}</td>
          <td style={tbStyle}>{arrNames}</td>
          <td style={tbStyle}><img width="128" height="128" src={src}/></td>
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
              <th style={{textAlign:"center",verticalAlign: "middle"}}>Delete</th>
            </tr>
          </thead>
          <tbody>
            {this.showTable()}
          </tbody>
        </Table>
      </div>
    )}
}
