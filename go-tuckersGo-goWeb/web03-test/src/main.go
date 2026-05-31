package main

import (
	"github.com/kyungseok-lee/learn-go-web/myapp"
	"github.com/kyungseok-lee/learn-go-web/utils"
	"net/http"
)

func main() {
	utils.Hello()
	utils.Say()
	//utils.foo()
	http.ListenAndServe(":3000", myapp.NewHttpHandler())
}
