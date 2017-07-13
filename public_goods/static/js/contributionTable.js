var ContributionTable = function (n_players,reward_player,contribution){

	if(n_players <= 0) {
		throw "Number of Players Must be Greater than 0."	
	};
	
	if(reward_player <= 0){
		throw "Reward Must be Greater than 0."
	};

	if (typeof(contribution)=="undefined"){
		this.rowPctCont = [0, .5, 1];
	} else {
		this.rowPctCont = [contribution/reward_player];
	}	
	
	
	this.colPctCont = [0, .5, 1];
	this.N = n_players;
	this.R = reward_player;	
	
	this.getColumnHeaders = function(){
		var col_header = document.createElement('thead');
		var header_row = document.createElement('tr');
		var first = document.createElement('th')
		first.innerHTML = '<em>' + contribution +' pts </em>';
		header_row.appendChild(first);

		for (var i = 0, len = this.colPctCont.length; i < len; i++){
			var val = this.colPctCont[i] * this.R;
			var th = document.createElement('th');
			th.innerHTML = val+' pts';
			header_row.appendChild(th);
		}

		var label_row = document.createElement('tr');
		label_row.innerHTML = '<th><em>If you contribute:</em></th><th colspan=' + this.colPctCont.length + '>and everyone else contributes:</th>';
				
		col_header.append(label_row);		
		col_header.append(header_row);
		
		return col_header;
	};
	
	this.getRowHeader = function(rowVal){

		var val = rowVal * this.R;
		var th = document.createElement('td');
		th.innerHTML = '<em>Estimated returns (pts):</em>';
		
		return th;
	};
	
	this.calcValue = function (p_i,p_g,R,N) {
		return (1-p_i)*R + 2/N*(p_i*R + (N-1)*p_g*R);
	};
	
	this.createTableBody = function(){

		var makeRow = function(rowValue){
			var tblRow = document.createElement('tr')
			tblRow.appendChild(this.getRowHeader(rowValue));			
			
			var cols = this.colPctCont;
			
			for (var i = 0, len = cols.length; i < len; i++) {
				var cell = document.createElement('td');
				var val_you = this.calcValue(rowValue, cols[i], this.R, this.N);
				var val_team = this.calcValue(cols[i], rowValue, this.R, this.N);
				cell.innerHTML = '<p style="padding:0; margin:0;">You:&nbsp;&nbsp;&nbsp;&nbsp;' 
					+ (val_you.toFixed(0) - this.R)
					+ '</p><p style="padding:0; margin:0;">Team:&nbsp;' 
					+ (val_team.toFixed(0) - this.R) + '</p>';
				tblRow.appendChild(cell);
			};
			
			return tblRow;
		}.bind(this);		
		
		var tblBody = document.createElement('tbody');
		var rows = this.rowPctCont;
		for (var i = 0, len = rows.length; i < len; i++) {
			tblBody.appendChild(makeRow(rows[i]));	
		};
		
		return tblBody;
	};
	
	this.formatTable = function () {
		var table = document.createElement('table');
		table.className = 'table';
		var tblBody = this.createTableBody();
		
		table.appendChild(this.getColumnHeaders());
		table.appendChild(tblBody);
		
		return table;
	};
	
	this.init = function (div) {
		div.append(this.formatTable());
	};
};