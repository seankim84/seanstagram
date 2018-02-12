import React from 'react'; 
import PropTypes from 'prop-types';
import styles from './styles.scss';
import PhotoActions from 'components/PhotoActions';
import PhotoComments from 'components/PhotoComments';

const FeedPhoto = (props, context) => { //헤더에는 이미지와 creator, location이 있다. 
    return(
        <div className={styles.feedPhoto}>
            <header>
                <img src={props.creator.profile_image || require("images/noPhoto.jpg")} 
                     alt={props.creator.username}
                     />
            <div>
                <span>{props.creator.username}</span>
                <span>{props.location}</span>
            </div>
            </header>
            <img src={props.file} alt={props.caption} />
           <div>
             <PhotoActions number={props.like_count} />
             <PhotoComments 
                caption ={props.caption}
                creator={props.creator.username}
                comments={props.comments}
             />    
           </div>
        </div>
    );
};

FeedPhoto.propTypes = { //최대한 명확하게 props를 부른다. 먼저 creator를 부름(creator의 오브젝트 확인)
        creator: PropTypes.shape({
            profile_image: PropTypes.string,
            username: PropTypes.string.isRequired
        }).isRequired,
        location: PropTypes.string.isRequired,
        file: PropTypes.string.isRequired,
        like_count: PropTypes.number.isRequired,
        caption:PropTypes.string.isRequired,
        comments: PropTypes.arrayOf(
            PropTypes.shape({
                message:PropTypes.string.isRequired,
                creator: PropTypes.shape({
                profile_image: PropTypes.string,
                username: PropTypes.string.isRequired
               }).isRequired
           })
        ).isRequired,
        created_at:PropTypes.string.isRequired
    };



export default FeedPhoto;