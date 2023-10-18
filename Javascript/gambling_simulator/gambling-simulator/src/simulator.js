import React, { Component } from 'react';

class DVDBouncingSimulator extends Component {
  constructor(props) {
    super(props);
    this.state = {
      x: 50,
      y: 50,
      dx: 5,
      dy: 5,
      text: "TEST",
      fontSize: 20,
      canvasWidth: 800,
      canvasHeight: 600,
    };
  }

  componentDidMount() {
    this.drawText();
  }

  drawText() {
    const { x, y, dx, dy, text, fontSize, canvasWidth, canvasHeight } = this.state;
    const canvas = this.refs.canvas;
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    const textWidth = ctx.measureText(text).width;
    const textHeight = fontSize;

    ctx.font = `${fontSize}px Arial`;
    ctx.fillText(text, x, y);

    if (x + textWidth + dx > canvasWidth || x + dx < 0) {
      this.setState({ dx: -dx });
    }

    // if (y + textHeight + dy > canvasHeight || y + dy < 0) {
    //   this.setState({ dy: -dy });
    // }

    // Adjust the top boundary check
    if (y + dy < 25) {
      this.setState({ dy: -dy });
      this.setState({ y: 0 });
    }

    const lowerBoundaryOffset = -10; // Change this value to your desired offset
    if (y + textHeight + dy > canvasHeight - lowerBoundaryOffset) {
      this.setState({ dy: -dy });
      this.setState({ y: canvasHeight - textHeight - lowerBoundaryOffset });
    }


    this.setState({ x: x + dx, y: y + dy });

    requestAnimationFrame(this.drawText.bind(this));
  }

  render() {
    return (
      <canvas ref="canvas" width={this.state.canvasWidth} height={this.state.canvasHeight} />
    );
  }
}

export default DVDBouncingSimulator;
