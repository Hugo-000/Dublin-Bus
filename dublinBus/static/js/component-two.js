import React from 'react'
import ReactDOM from 'react-dom'


function ComponentTwo(props) {
    return <h1>Hello, {props.name}, I am component two!</h1>;
}

export default () => {
    const element = <ComponentTwo name="you" />;
    const target = document.getElementById('component-two')

    if (!target) return;

    ReactDOM.render(element, target);
}
