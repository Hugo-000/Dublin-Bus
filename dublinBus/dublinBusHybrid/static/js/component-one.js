import React, { Component } from 'react'
import ReactDOM from 'react-dom'


function ComponentOne(props) {
    return <h1>Hello, {props.name}, I am component one!</h1>;
}

export default () => {
    const element = <ComponentOne name="you" />;
    const target = document.getElementById('component-one')
    
    if (!target) return;

    ReactDOM.render(element, target);
}
