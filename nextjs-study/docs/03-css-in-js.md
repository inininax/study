# Next App
## CSS-in-JS
```javascript
function HiThere() {
  return <p style={{color: 'red'}}>hi there</p>
}
export default HiThere
```

```javascript
function HelloWorld() {
  return (
    <div>
      Hello world
      <p>scoped!</p>
      <style jsx>{`
        p {
          color: blue;
        }
        div {
          background: red;
        }
        @media (max-width: 600px) {
          div {
            background: blue;
          }
        }
      `}</style>
      <style global jsx>{`
        body {
          background: black;
        }
      `}</style>
    </div>
  )
}
export default HelloWorld
```