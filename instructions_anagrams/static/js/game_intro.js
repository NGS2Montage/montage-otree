var Tour = function (){
        this.intro = introJs();
        this.intro.setOptions({
          	disableInteraction: true,
          	exitOnOverlayClick: false,
          	exitOnEsc: false,
          	showStepNumbers: false,
          	scrollToElement: true,
            steps: [
              { 
              	 element: document.querySelector('#your-letters'),
                intro: "These are <strong>your</strong> letters. You will receive 3 letters that appear in <span class='label label-info'>BLUE</span> panels.",
                position: 'auto'
              },
              {
                element: document.querySelector('#get-team-letters'),
                intro: "You can request more letters from your teammates by clicking here.",
                position: 'auto'
              },
              {
                element: document.querySelector('#team-letters'),
                intro: "Letters that you request will appear here. They will remain <span class='label label-warning'>ORANGE</span> until they are copied to you by your teammates. Once copied, they turn <span class='label label-success'>GREEN</span> and you can use them to create words. For example, you can spell 'ROLE', but not 'REAL' because the A is unavailable.",
                position: 'auto'
              },
              {
                element: document.querySelector('#word-input-group'),
                intro: 'You can either click on the letter or type in the words you can make in this box. Form a valid English word that is <strong>3 letters or longer</strong> and enter it into the submission box.</strong> For example, the letters R,O,L can be used to spell the word “ROLL” (case does not matter: roll = ROLL = roLL, etc.).  Remember, you can only type or click on <span class="label label-info">BLUE</span> or <span class="label label-success">GREEN</span> letters. Then click submit.',
                position: 'auto'
              },
              {
                element: document.querySelector('#word-panel'),
                intro: 'Words submitted by you and your teammates appear in this window. We encourage your to duplicate as many words as possible from your teammates. Duplicate words earn 2x points.',
                position: 'auto'
              },
              {
                element: document.querySelector('#score-div'),
                intro: 'We show the score here. You want to increase this word count as much as possible.',
                position: 'auto'
              },
              {
                element: document.querySelector('#copy-letters-div'),
                intro: "Just as you request letters from your team, your teammates will request letters from you. Click on the buttons in this window to <strong><em>copy</em></strong> your letters to another teammate's window. This turns <strong>their</strong> letter from <span class='label label-warning'>ORANGE</span> to <span class='label label-success'>GREEN</span>.",
                position: 'top'
              },
              {
                element: document.querySelector('#info-detail'),
                intro: "Lastly, you can view these instructions again here while playing.",
                position: 'auto'
              },
              {
                element: document.querySelector('.next-button'),
                intro: "<strong>Please click next to proceed.</strong> The game will begin after a quick quiz.",
                position: 'top'
              },
            ]
          });
          this.intro.start();
          
          this.next = function () {
          	this.intro.nextStep();
          };
          
          $('.introjs-skipbutton').hide();

    		 this.intro.onafterchange(function(el){
    		 	        
        		if (this._introItems.length - 1 == this._currentStep || this._introItems.length == 1) {
            	//$('.introjs-skipbutton').show();
            	$('.introjs-disableInteraction').removeClass('introjs-disableInteraction');
            	
        		} 
    		 });
};


//tour = new Tour();