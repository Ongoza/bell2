import React from 'react';
import {Table, Nav, Pager, NavItem, Panel, Tooltip, OverlayTrigger , Button, ButtonGroup, Form, Alert, FormControl, FormGroup, Col, ControlLabel} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'

export default class Logs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      imageURL: '',
      result:"",
      resultTr: false,
      alertType:"info"
    };
    this.text = "Loading data..."
    this.linesPerPage = 20
    this.start=0
    this.curPage = 1
    this.end=this.start+this.linesPerPage
    this.total = this.end
    this.totalPages = this.total/this.linesPerPage
    this.activeKey='../log/camera_webCamera_face.log?'
    this.activePage = 'start='+this.start+'&end='+this.end
    this.takeLogData = this.takeLogData.bind(this)

  }

  componentDidMount() { this.resultTr=false; this.takeLogData();
    this.timer = setInterval(this.takeLogData, 5000);
  }

  componentWillUnmount() { if(this.timer){ clearInterval(this.timer) }
  }

  // this.timerUpdate(){
  //
  // }

  handleErrors(response) {
      if (!response.ok) {throw Error(response.statusText)}
      return response;
  }

  takeLogData(){
    console.log("start take log")
    let str_auth = 'Basic ' + localStorage.getItem('id_token')
      fetch(this.activeKey+this.activePage,{headers: new Headers({'Authorization': str_auth})})
      .then(this.handleErrors)
      .then((response) => {
        // console.log("server ansver0=",response)
        response.text().then((body) => {
          // console.log("server body=",body)
          let lastNumber = 0, strHtml=""
          // console.log("last line ",lastNumber, body)
          if(body.lastIndexOf("\n")>0) {
            let strInt = body.substring(body.lastIndexOf("Total lines===")+14)
            this.total = parseInt(strInt)
            strHtml = body.substring(0, body.lastIndexOf("Total lines===")-1)
            this.totalPages = Math.floor(this.total/this.linesPerPage)+1
            this.curPage = Math.floor(this.end/this.linesPerPage)
            console.log("last line ",strInt,this.total,this.totalPages,this.curPage,this.start)
          }
          strHtml= strHtml.replace(/(?:\r\n|\r|\n)/g, '<br />');
          // let strHtml= body
          strHtml = strHtml.replace(/<img/g,"<img width=\"64\" height=\"64\" ")
          this.refs.log_body.innerHTML = strHtml
          this.setState({ resultTr: !this.state.resultTr});
          // this.setState({alertType:body.Type})
        });
      })
      .catch((err)=>{console.log("Error connect to Server") })
}
  clearLog(){
    let str_auth = 'Basic ' + localStorage.getItem('id_token')
    fetch('../clearLog?'+this.activeKey,{headers: new Headers({'Authorization': str_auth})})
    .then(this.handleErrors)
    .then((response) => {
      // console.log("server ansver0=",response)
      this.takeLogData();
    })
    .catch((err)=>{console.log("Error connect to Server") })
  }

  handleSelectTab(k){
    console.log("tab click",k)
    this.activeKey = k
    this.start=0
    this.end = this.start + this.linesPerPage
    this.activePage = 'start='+this.start+'&end='+this.end
    this.takeLogData()
    // this.state.resultTr = !this.state.resultTr
  }

  pageChange(e){
    // console.log("click=",e)
    switch(e) {
      case "first": this.start=0; break;
      case "prev":
        let tr1 = this.start - this.linesPerPage
        if( tr1 > 0 ){this.start=tr1
        }else{this.start=0}
        break;
      case "next":
      let tr2 = this.start + this.linesPerPage
        if(tr2 < this.total ){ this.start=tr2}
        break;
      case "last":
        this.start = this.total-this.linesPerPage
        break;
      }
    this.end = this.start + this.linesPerPage
    this.activePage = 'start='+this.start+'&end='+this.end
    // console.log("activePage=",this.activePage)
    this.takeLogData()
  }

  render() {
    return (
      <div>
        {this.state.resultTr}
        <div style={{fontSize:"200%"}} >Logs &nbsp;&nbsp;
          <Button bsStyle="primary" onClick={this.clearLog} name ="btUpdate" key ="bt" >Clear log</Button>
        </div>
          <Nav bsStyle="tabs" activeKey={this.activeKey} onSelect={k => this.handleSelectTab(k)}>
          <NavItem eventKey={'../log/camera_webCamera_face.log?'} >Events</NavItem>
          <NavItem eventKey={'../log/camera_webCamera.log?'} >Camera</NavItem>
          <NavItem eventKey={'../log/camera_manager.log?'} >Cameras manager</NavItem>
          <NavItem eventKey={'../log/webServer.log?'} >Server</NavItem>
        </Nav>
        <Pager onSelect={k=>this.pageChange(k)} bsSize="small">
          <Pager.Item eventKey ="first" name="first">1</Pager.Item>
          <Pager.Item eventKey="prev" >Prev</Pager.Item>
          <Pager.Item eventKey="cur">{"Current page: "+this.curPage}</Pager.Item>
          <Pager.Item eventKey="next" >Next</Pager.Item>
          <Pager.Item eventKey="last" >{this.totalPages}</Pager.Item>
        </Pager>
        <div key="log_body" ref="log_body" id="log_body"> </div>
      </div>
    )}
}
