(this["webpackJsonpbaboon-tracking-status"]=this["webpackJsonpbaboon-tracking-status"]||[]).push([[0],{166:function(t,e,a){"use strict";a.r(e);var n=a(10),r=a.n(n),s=a(57),i=a.n(s),c=(a(62),a(25)),o=a(26),u=a(28),l=a(27),p=(a(63),a(13)),d=a.n(p),b=a(29),v=a(14),h=a(41),g=a(17),f=a(6),j=function(t){Object(u.a)(a,t);var e=Object(l.a)(a);function a(t){var n;return Object(c.a)(this,a),(n=e.call(this,t)).state={errorRateData:{},learningData:{}},n}return Object(o.a)(a,[{key:"getFirebaseDatabase",value:function(){return g.a.apps.length?g.a.app():g.a.initializeApp({apiKey:"AIzaSyB83cPhCkA-xv-K6UOZAc0zuH7sxDuxHlE",authDomain:"baboon-cli-1598770091002.firebaseapp.com",databaseURL:"https://baboon-cli-1598770091002-default-rtdb.firebaseio.com/"}),g.a.database()}},{key:"parseDate",value:function(t){var e=t.split("-"),a=Object(v.a)(e,2),n=a[0],r=a[1],s=parseInt(n.substr(0,4)),i=parseInt(n.substr(4,2))-1,c=parseInt(n.substr(6,2)),o=parseInt(r.substr(0,2)),u=parseInt(r.substr(2,2)),l=parseInt(r.substr(4,2));return Date.UTC(s,i,c,o,u,l)}},{key:"getChartData",value:function(){var t=Object(b.a)(d.a.mark((function t(){var e,a,n,r,s,i,c,o,u,l,p;return d.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e=this.getFirebaseDatabase(),a=e.ref("metrics"),n=a.child("input"),r=n.child("latest"),t.next=6,r.get();case 6:return s=t.sent.val(),i=n.child(s),c=this.parseDate(s),t.next=11,i.get();case 11:return o=t.sent.val(),u=o.map((function(t,e){var a=t.true_positive+t.false_negative;return{x:e/30,y:(t.false_negative+t.false_positive)/a}})),l=btoa(["Frame, True Positive, False Negative, False Positive"].concat(o.map((function(t,e){return"".concat(e,", ").concat(t.true_positive,", ").concat(t.false_negative,", ").concat(t.false_positive)}))).join("\n")),p=Math.round(1e4*u.map((function(t){return t.y})).reduce((function(t,e){return t+e}))/u.length)/100,t.abrupt("return",{data:u,csv:l,averageErrorRate:p,latestUpdate:c});case 16:case"end":return t.stop()}}),t,this)})));return function(){return t.apply(this,arguments)}}()},{key:"getLearningData",value:function(){var t=Object(b.a)(d.a.mark((function t(){var e,a,n,r,s,i,c,o,u,l,p,b,h,g,f;return d.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e=this.getFirebaseDatabase(),a=e.ref("optimize"),n=a.child("input"),r=n.child("latest"),s=n.child("losses"),t.next=7,r.get();case 7:return i=t.sent.val(),t.next=10,s.get();case 10:if(!(c=t.sent.val())){t.next=20;break}return o=Object(v.a)(Object.entries(c).slice(-1)[0],1),u=o[0],l=this.parseDate(u),p=Object.entries(c).map((function(t,e){return{x:e,y:Object(v.a)(t,2)[1]}})),b=Object.entries(c).map((function(t){return Object(v.a)(t,1)[0]===i?"#90cd8a":"rgba(0, 0, 0, 0.1)"})),h=0,p.length>1&&(g=Object.entries(c).filter((function(t){return Object(v.a)(t,1)[0]===i})).map((function(t){return Object(v.a)(t,2)[1]}))[0],h=Math.round(1e4*(p[0].y-g)/p[0].y)/100),f=btoa(["Iteration, Loss"].concat(p.map((function(t){return"".concat(t.x,", ").concat(t.y)}))).join("\n")),t.abrupt("return",{csv:f,data:p,percentImprovement:h,latestUpdate:l,dataPointBackgroundColor:b});case 20:return t.abrupt("return",{});case 21:case"end":return t.stop()}}),t,this)})));return function(){return t.apply(this,arguments)}}()},{key:"componentDidMount",value:function(){var t=Object(b.a)(d.a.mark((function t(){var e,a;return d.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,this.getChartData();case 2:return e=t.sent,t.next=5,this.getLearningData();case 5:a=t.sent,this.setState({averageErrorRate:e.averageErrorRate,errorRateCSV:e.csv,errorRateData:{datasets:[{label:"Error Rate",data:e.data,pointRadius:0}]},errorRateLastUpdated:e.latestUpdate,learningData:{datasets:[{label:"Loss",data:a.data,pointBackgroundColor:a.dataPointBackgroundColor}]},learningCSV:a.csv,learningPercentImprovement:a.percentImprovement,learningLatestUpdate:a.latestUpdate});case 7:case"end":return t.stop()}}),t,this)})));return function(){return t.apply(this,arguments)}}()},{key:"render",value:function(){var t=new Date(this.state.errorRateLastUpdated||0),e=new Date(this.state.learningLatestUpdate||0);return Object(f.jsxs)("div",{children:[Object(f.jsx)(h.Line,{data:this.state.errorRateData,options:{legend:{display:!1},title:{display:!0,text:"Error Rate vs. Seconds"},scales:{xAxes:[{type:"linear",scaleLabel:{display:!0,labelString:"Seconds"}}],yAxes:[{type:"linear",ticks:{callback:function(t,e,a){return Math.round(100*t)+"%"}},scaleLabel:{display:!0,labelString:"Error Rate"}}]}}}),Object(f.jsxs)("p",{children:["Last Updated: ","".concat(t.toLocaleDateString()," ").concat(t.toLocaleTimeString())]}),Object(f.jsxs)("p",{children:["Average Error Rate: ",this.state.averageErrorRate,"%"]}),Object(f.jsx)("a",{download:"ErrorRate.csv",href:"data:text/csv;base64,".concat(this.state.errorRateCSV),children:"Download CSV"}),Object(f.jsx)(h.Line,{data:this.state.learningData,options:{legend:{display:!1},title:{display:!0,text:"Loss vs. Iterations"},scales:{xAxes:[{type:"linear",scaleLabel:{display:!0,labelString:"Iterations"}}],yAxes:[{type:"linear",scaleLabel:{display:!0,labelString:"Loss"}}]}}}),Object(f.jsxs)("p",{children:["Last Updated: ","".concat(e.toLocaleDateString()," ").concat(e.toLocaleTimeString())]}),Object(f.jsxs)("p",{children:["Percent Improvement: ",this.state.learningPercentImprovement,"%"]}),Object(f.jsx)("a",{download:"Learning.csv",href:"data:text/csv;base64,".concat(this.state.learningCSV),children:"Download CSV"})]})}}]),a}(r.a.Component),x=function(t){Object(u.a)(a,t);var e=Object(l.a)(a);function a(){return Object(c.a)(this,a),e.apply(this,arguments)}return Object(o.a)(a,[{key:"componentDidMount",value:function(){document.title="Baboons on the Move Status"}},{key:"render",value:function(){return Object(f.jsx)("div",{children:Object(f.jsx)(j,{})})}}]),a}(r.a.Component),m=function(t){t&&t instanceof Function&&a.e(3).then(a.bind(null,167)).then((function(e){var a=e.getCLS,n=e.getFID,r=e.getFCP,s=e.getLCP,i=e.getTTFB;a(t),n(t),r(t),s(t),i(t)}))};i.a.render(Object(f.jsx)(r.a.StrictMode,{children:Object(f.jsx)(x,{})}),document.getElementById("root")),m()},62:function(t,e,a){},63:function(t,e,a){}},[[166,1,2]]]);
//# sourceMappingURL=main.5fd0096f.chunk.js.map