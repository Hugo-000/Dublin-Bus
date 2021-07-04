'use strict';

const e = React.createElement;
  
  class LikeButton extends React.Component {
    constructor(props) {
      super(props);
      this.state = { liked: false };
    }
  
    render() {
      if (this.state.liked) {
        return 'Nice! So do I!';
      }
  
      return (
        <button onClick={() => this.setState({ liked: true })}>
          Do you like react? Yes?
        </button>
      );
    }
  }
  
  const domContainer = document.querySelector('#like_button_container');
  ReactDOM.render(<LikeButton />, domContainer);