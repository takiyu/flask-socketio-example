var socket = io.connect('/test');

var Button = ReactBootstrap.Button;
var Popover = ReactBootstrap.Popover;

var RangeInput = React.createClass({
    getInitialState() {
      return {
        value: 1,
      };
    },
    componentDidMount() {
    },
    handleChange(e) {
      var val = e.target.value;
      if (this.state.value != val) {
        this.setState({value: val});
        socket.emit('update', {range: val})
      }
    },
    render() {
      return (<input type="range" 
               min="0" max="100" step="1"
               className="slider-selection"
               value={this.state.value} 
               onChange={this.handleChange} />);
    }
});


var ButtonInput = React.createClass({
    componentDidMount() {
    },
    handleClick() {
      socket.emit('update', {button: true})
    },
    render() {
      return (
          <Button bsStyle="primary" bsSize="normal"
           onClick={this.handleClick}>Button</Button>
      );
    }
});


var Message = React.createClass({
    getInitialState() {
      return {
        message: 'Message',
      };
    },
    componentDidMount() {
    },
    setMessage(message) {
      this.setState({message: message});
    },
    render() {
      return (
        <Popover id={0} style={{maxWidth: 400}}>
          {this.state.message}
        </Popover>
      );
    }
});


var MainView = React.createClass({
    componentDidMount() {
      // socket.io events
      socket.on('connect', this.onConnect);
      socket.on('response', this.onResponse);
    },
    onConnect() {
      console.log('Connect');
    },
    onResponse(data) {
      this.refs.message.setMessage(data.message);
    },
    render() {
      return (
        <div className="center-block">
          <div className="container">
            <div className="well"
                 style={{maxWidth: 900, margin: '30px'}}>
              <div className="row">
                <div className="col-xs-5">
                  <RangeInput />
                </div>
                <div className="col-xs-2">
                  <ButtonInput />
                </div>
                <div className="col-xs-5">
                  <Message ref="message" />
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    }
});


ReactDOM.render(
  <MainView />,
  document.getElementById('content')
);
