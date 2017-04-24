var Tour = function (){
        this.intro = introJs();
        this.intro.setOptions({
          	disableInteraction: false,
          	exitOnOverlayClick: true,
          	exitOnEsc: true,
          	showStepNumbers: false,
          	scrollToElement: true,
            steps: [
              { 
              	 element: document.querySelector('#tip'),
                intro: "Tip: Before submitting your number, click view risk/reward. This will tell you how much you could gain or lose depending on what your teammates choose.",
                position: 'auto'
              },
            ]
          });
          this.intro.start();
          
          this.next = function () {
          	this.intro.nextStep();
          };
          
          

    		 this.intro.onafterchange(function(el){
    		 	        
        		if (this._introItems.length - 1 == this._currentStep || this._introItems.length == 1) {
            	$('.introjs-skipbutton').show();
            	//$('.introjs-disableInteraction').removeClass('introjs-disableInteraction');
            	
        		} 
    		 });
};


var tour = new Tour();