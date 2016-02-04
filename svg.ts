class Workflow {

  nodes : Array<SvgNode> ;
  connections : Array<Connection> ;

  constructor(svg : SVGSVGElement, data) {
    this.nodes = [];
    this.connections = [];
    this.loadNodes(svg,data);
    this.loadConnections(svg,data);
  }

  loadNodes(svg : SVGSVGElement, data) : void {
    for( var node of data.nodes ) {
      var n = new SvgNode(svg,node);
      this.nodes.push(n);
    }
  }

  findNodeById(id : number) : SvgNode {
    for(var i=0;i<this.nodes.length;i++) {
      if ( this.nodes[i].id == id ) {
        return this.nodes[i];
      }
    }
    return null;
  }

  loadConnections(svg : SVGSVGElement, data) : void {
    for (var connection of data.connections ) {
      var src = this.findNodeById(data.src);
      var dst = this.findNodeById(data.dst);
      if( src != null && dst != null ) {
        var cnx = new Connection(svg,src,dst);
        this.connections.push(cnx);
      }
    }
  }
}

class SvgElement {

  svg : SVGSVGElement ;
  x : number ;
  y : number ;

  connectors : Array<Connector> ;

  constructor(svg : SVGSVGElement) {
    this.svg = svg ;
  }

  createElementNS(name : string, attributs ) : SVGDefsElement {
    var svgNS = "http://www.w3.org/2000/svg";
    var elem = document.createElementNS(svgNS,name);
    for( var item in attributs ) {
      elem.setAttributeNS(null, item, attributs[item] );
    }
    return (<SVGDefsElement>elem) ;
  }

  getSize() {
    return this.svg.getBoundingClientRect();
  }


}

class SvgNode extends SvgElement {

  name : string ;
  id : number ;
  g : SVGDefsElement ;
  circle : SVGDefsElement ;

  constructor( svg : SVGSVGElement, data ) {
    super(svg);
    this.id = data.id ;
    this.name = data.name ;

    this.generate();

    for( var con of data.connectors ) {
      var tmp = new Connector( svg, con );
      this.connectors.push(tmp);
    }
  }

  //Generate svg code
  generate() {
    var svgNS = "http://www.w3.org/2000/svg";
    this.g = <SVGDefsElement>document.createElementNS(svgNS,"g");
    this.circle = this.createElementNS("rect", { 'rx' : 10, 'ry' : 10,
      'width' : 180, 'height' : 200,
      'fill' : '#848484', 'stroke' : 'black',
       });

    this.g.setAttributeNS(null,'onmousedown',"onMouseDown(evt);");
    //mouse selection is not match with g element !
    (<any>this.circle).data = this ;
    this.svg.appendChild(this.g);
    this.g.appendChild(this.circle);
    this.addText(this.name);
  }

  addText(txt:string) {
    var text = this.createElementNS("text", { 'x':15, 'y':20, 'fill' : 'black' });
    text.textContent = txt ;
    this.g.appendChild(text);
  }

  addImage( url : string ) {
    var img = this.createElementNS("image", { 'x' : 10, 'y' : 40, 'width' : 128, 'height' : 128 });
    img.setAttributeNS('http://www.w3.org/1999/xlink', "href", url );
    this.g.appendChild(img);
  }

  move( x : number, y : number ) {
    var pt = this.svg.createSVGPoint();
    pt.x = x ; pt.y = y ;
    var pt_loc = pt.matrixTransform(this.svg.getScreenCTM().inverse())
    this.x = pt_loc.x - this.getSize().width / 2 ;
    this.y = pt_loc.y - this.getSize().height / 2 ;
    var translate = '(' + this.x + ',' + this.y  + ')';
    this.g.setAttribute('transform','translate' + translate )
  }

  getSize() {
    return this.g.getBoundingClientRect();
  }

  getPosition() {
    return { 'x' : + this.x + this.getSize().width / 2, 'y' : + this.y + this.getSize().height / 2 }
  }

  selected( value : boolean ) {
    var color = '#848484' ;
    if( value )
      color = '#FF8000' ;
    this.circle.setAttributeNS(null,"fill",color);
  }
}

class Connector extends SvgElement {

  name : string ;

  constructor( svg : SVGSVGElement, data ) {
    super(svg);
    this.name = data.name ;
  }
}

class ConnectorIn extends Connector {

  connection : Connection ;

  constructor(svg : SVGSVGElement, data ) {
    super(svg,data);
  }
}

class ConnectorOut extends Connector {

  connections : Array<Connection> ;

  constructor(svg : SVGSVGElement, data ) {
    super(svg,data);
  }
}

class Connection extends SvgElement {
  connector_src : Connector ;
  connector_dst : Connector ;
  path : SVGPathElement ;

  constructor( svg : SVGSVGElement, src : SvgNode, dst : SvgNode ) {
    super(svg);
    this.connector_src = src ;
    this.connector_dst = dst ;
    this.path = <SVGPathElement>this.createElementNS("path", {
      'fill' : 'none',
      'stroke' : 'black',
    });
    svg.appendChild(this.path);
  }

  update = function() {
    var p1 = this.connector_src.getPosition();
    var p2 = this.connector_dst.getPosition();
    var pm = { 'x' : p1.x + ( p2.x - p1.x ) / 2, 'y' : p1.y + ( p2.y - p1.y ) / 2 };
    var path_d = "M" + p1.x + ',' + p1.y + ' '
      + 'C' + pm.x + ',' + p1.y + ' '
      + pm.x + ',' + p2.y + ' '
      +  p2.x + ',' + p2.y ;
    this.path.setAttributeNS(null,'d', path_d);
  }
}
