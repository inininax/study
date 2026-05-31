function LoadingSplash(param) {
	this.opts = Ext.merge({}, param, {
		wrapper: 'loadingSplash',
		top: 'loadingSplashTop',
		bottom: 'loadingSplashBottom',
		items: 'loadingSplashCircles',
		theme: 'triton'
	});

	this.wrapper = null;
	this.top = null;
	this.bottom = null;
	this.items = null;
}

LoadingSplash.prototype.appendHead = function () {
	// Ext.ieVersion
	var href = './' + (Ext.isIE && Ext.isIE9m ? 'loader_ie.css' : 'loader.css');
	var head = Ext.getHead();
	head.createChild({
		tag: 'link',
		href: href,
		rel: 'stylesheet',
		type: 'text/css'
	});
};

LoadingSplash.prototype.appendBody = function () {
	var opts = this.opts;
	var wrapper = opts.wrapper;
	var top = opts.top;
	var bottom = opts.bottom;
	var items = opts.items;
	var theme = opts.theme;

	// class : triton, napture, ios

	var template = '<div id="{0}" class="{4}">';
	template += '	<div id="{1}"></div>';
	template += '	<div id="{2}"></div>';
	template += '	<div class="loading-fading-circle" id="{3}">';
	template += '		<div class="loading-circle-2 loading-circle"></div>';
	template += '		<div class="loading-circle-3 loading-circle"></div>';
	template += '		<div class="loading-circle-1 loading-circle"></div>';
	template += '		<div class="loading-circle-4 loading-circle"></div>';
	template += '		<div class="loading-circle-5 loading-circle"></div>';
	template += '		<div class="loading-circle-6 loading-circle"></div>';
	template += '		<div class="loading-circle-7 loading-circle"></div>';
	template += '		<div class="loading-circle-8 loading-circle"></div>';
	template += '		<div class="loading-circle-9 loading-circle"></div>';
	template += '		<div class="loading-circle-10 loading-circle"></div>';
	template += '		<div class="loading-circle-11 loading-circle"></div>';
	template += '		<div class="loading-circle-12 loading-circle"></div>';
	template += '	</div>';
	template += '</div>';

	var html = Ext.util.Format.format(template, wrapper, top, bottom, items, theme);

	var body = Ext.getBody();
	body.createChild(html);

	this.wrapper = Ext.get(wrapper);
	this.top = Ext.get(top);
	this.bottom = Ext.get(bottom);
	this.items = Ext.get(items);
};

LoadingSplash.prototype.create = function () {
	// this.appendHead();
	this.appendBody();
};

LoadingSplash.prototype.destroy = function () {
	if (Ext.supports.Transitions) {
		this.destroyTransitions();
		return;
	}

	this.destroyAnim();
};

LoadingSplash.prototype.destroyTransitions = function () {
	this.top.on('transitionend', this.wrapper.destroy, this.wrapper, {
		single: true
	});

	this.wrapper.addCls('app-loaded');
};

LoadingSplash.prototype.destroyAnim = function () {
	this.circles.destroy();

	Ext.create('Ext.fx.Anim', {
		target: this.top,
		duration: 500,
		from: {
			top: 0
		},
		to: {
			top: this.top.getHeight() * -1
		}
	});

	Ext.create('Ext.fx.Anim', {
		target: this.bottom,
		duration: 500,
		from: {
			bottom: 0
		},
		to: {
			bottom: this.bottom.getHeight() * -1
		},
		listeners: {
			single: true,
			delay: 500,
			scope: this.wrapper,
			afteranimate: this.wrapper.destroy
		}
	});
};