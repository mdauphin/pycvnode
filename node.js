function Node(name, connectors){
  this.name = name ;
  this.connectors = connectors;
}

Node.prototype.render = function( div ) {
  console.log("render " + this.name );
  div.addClass('node');
  var html = "<h2>" + this.name  + "</h2>" ;
  this.connectors.map(function(v) { html += v.render(); });
  div.html(html);
};

Node.prototype.serialize = function() {
  var connectors = [];
  this.connectors.map( function(v) { connectors.push( v.serialize() ); } );
  var ret = { 'name': this.name, 'connectors' : connectors };
  return JSON.stringify(ret);
};

Node.prototype.deserialize = function(data) {
  this.name = data['name'];
  this.connectors = data['connectors'].map( function(v) {
    if ( v.direction == 'in' )
      return new ConnectorIn(v['name']);
    else
      return new ConnectorOut(v['name']);
  } );
};

//----- Connector ----------

function Connector(name){
  this.name = name ;
}

Connector.prototype.serialize = function() {
  var ret = { 'name': this.name };
  return ret ;
}

//----- ConnectorIn ----------

function ConnectorIn(name){
  Connector.call(this, name);
}

ConnectorIn.prototype = Object.create(Connector.prototype);

ConnectorIn.prototype.render = function( div ) {
  return '<div class="connector_in">' + this.name + '</div>';
};

//----- ConnectorOut ----------

function ConnectorOut(name){
  Connector.call(this, name);
}

ConnectorOut.prototype = Object.create(Connector.prototype);

ConnectorOut.prototype.render = function( div ) {
  return '<div class="connector_out">' + this.name + '</div>';
};


function Hello() {
  console.log('hello');
}
