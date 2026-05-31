'use strict';

// 기본
import gulp from 'gulp';
import gutil from 'gulp-util';

// 플러그인
import cleanCSS from 'gulp-clean-css';
import htmlmin from 'gulp-htmlmin';
import imagemin from 'gulp-imagemin';
import del from 'del';
import babel from 'gulp-babel';
import nodemon from 'gulp-nodemon';
import Cache from 'gulp-file-cache';
import webpack from 'gulp-webpack';
import webpackConfig from './webpack.config.js';
import browserSync from 'browser-sync';

// 디렉토리 정의
const DIR = {
	SRC: 'src',
	DEST: 'dist'
};

const SRC = {
	JS: DIR.SRC + '/js/*.js',
	CSS: DIR.SRC + '/css/*.css',
	HTML: DIR.SRC + '/*.html',
	IMAGES: DIR.SRC + '/images/*',
	SERVER: 'server/**/*.js'
};

const DEST = {
	JS: DIR.DEST + '/js',
	CSS: DIR.DEST + '/css',
	HTML: DIR.DEST + '/',
	IMAGES: DIR.DEST + '/images',
	SERVER: 'app'
};

// cache
let cache = new Cache();

// gulp clean (clean)
gulp.task('clean', () => {
	return del.sync([DIR.DEST]);
});

// gulp webpack
gulp.task('webpack', () => {
	return gulp.src('src/js/main.js')
		.pipe(webpack(webpackConfig))
		.pipe(gulp.dest('dist/js'));
});

// gulp css (minify css)
gulp.task('css', () => {
	return gulp.src(SRC.CSS)
		.pipe(cleanCSS({
			compatibility: 'ie8'
		}))
		.pipe(gulp.dest(DEST.CSS));
});

// gulp html (minify html)
gulp.task('html', () => {
	return gulp.src(SRC.HTML)
		.pipe(htmlmin({
			collapseWhitespace: true
		}))
		.pipe(gulp.dest(DEST.HTML))
});

// gulp image (compress images)
gulp.task('images', () => {
	return gulp.src(SRC.IMAGES)
		.pipe(imagemin())
		.pipe(gulp.dest(DEST.IMAGES));
});

// gulp babel
gulp.task('babel', () => {
	return gulp.src(SRC.SERVER)
		.pipe(cache.filter())
		.pipe(babel({
			presets: ['es2015']
		}))
		.pipe(cache.cache())
		.pipe(gulp.dest(DEST.SERVER));
});

// gulp watch
gulp.task('watch', () => {
	let watcher = {
		webpack: gulp.watch(SRC.JS, ['webpack']),
		css: gulp.watch(SRC.CSS, ['css']),
		html: gulp.watch(SRC.HTML, ['html']),
		images: gulp.watch(SRC.IMAGES, ['images']),
		babel: gulp.watch(SRC.SERVER, ['babel'])
	};

	let notify = (event) => {
		gutil.log('File', gutil.colors.yellow(event.path), 'was', gutil.colors.magenta(event.type));
	};

	for (let key in watcher) {
		watcher[key].on('change', notify);
	}
});

// gulp start
gulp.task('start', ['babel'], () => {
	return nodemon({
		script: DEST.SERVER + '/main.js',
		watch: DEST.SERVER
	});
});

// gulp browser-sync
gulp.task('browser-sync', () => {
	browserSync.init(null, {
		proxy: "http://localhost:3000",
		files: ["dist/**/*.*"],
		port: 7000
	})
});

// gulp (default)
gulp.task('default', [
	'clean',
	'webpack', 'css', 'html', 'images',
	'watch', 'start', 'browser-sync'
], () => {
	gutil.log('Gulp is running');
});