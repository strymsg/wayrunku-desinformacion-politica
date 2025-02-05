"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

locators = {
    'profiles': {
        ### profile info ###
        'followingCount': {
            'stype': 'xpath',
            'value': '//strong[@title="Following"][@data-e2e="following-count"]'
        },
        'followersCount': {
            'stype': 'xpath',
            'value': '//strong[@title="Followers"][@data-e2e="followers-count"]'
        },
        'likesCount': {
            'stype': 'xpath',
            'value': '//strong[@title="Likes"][@data-e2e="likes-count"]'
        },
        'videoElement': {
            'stype': 'css',
            'value': 'div[data-e2e="user-post-item"]'
        },
        'videoViews': {
            'stype': 'css',
            'value': 'strong[data-e2e="video-views"]'
        }
    },
    'videos': {
        'tags': {
            'stype': 'css',
            'value': 'a[data-e2e="search-common-link"]'
        },
        'likeCount': {
            'stype': 'css',
            #'value': '[data-e2e="browse-like-count"]' # pantallas grandes
            'value': 'strong[data-e2e="like-count"]'
        },
        'pinnedBadge': {
            'stype': 'xpath',
            'value': '//div[@data-e2e="video-card-badge"]'
        },
        'commentCount': {
            'stype': 'css',
            #'value': 'strong[data-e2e="browse-comment-count"]' # pantallas grandes
            'value': 'strong[data-e2e="comment-count"]'
        },
        'savedCount': {
            'stype': 'css',
            'value': 'strong[data-e2e="undefined-count"]'
        },
        'shareCount': {
            'stype': 'css',
            'value': '[data-e2e="share-count"]'
        },
        'description': {
            #'stype': 'xpath',
            #'value': '//span[@data-e2e="new-desc-span"]'
            'stype': 'css',
            'value': 'div.css-bs495z-DivWrapper.e1mzilcj0'
        },
        'date': {
            'stype': 'css',
            'value': 'span[data-e2e="browser-nickname"] span:last-child'
        }
    },
    'comments': {
        'usernameL1': {
            'stype': 'xpath',
            'value': '//div[@data-e2e="comment-username-1"]/div/a'
        },
        'usernameProfileLlinkL1': {
            'stype': 'xpath',
            'value': '//div[@data-e2e="comment-username-1"]/div/a'
        },
        'L1' : {
            'stype': 'xpath',
            'value': '//div[@class="css-1k8xzzl-DivCommentContentWrapper e1oxncge2"]//span[@data-e2e="comment-level-1"]'
            #'value': '//div[@class="css-1i7ohvi-DivCommentItemContainer eo72wou0"]//p[@data-e2e="comment-level-1"]'
        },
        'likesCountL1': {
            'stype': 'xpath',
            'value': '//div[@class="css-1ivw6bb-DivCommentSubContentSplitWrapper e1oxncge5"]/div/div/span'
            #'value': '//div[@class="css-ex1vmp-DivCommentContentContainer e1g2efjf0"]//p[@data-e2e="comment-level-1"]/following-sibling::p//span[@data-e2e="comment-like-count"]'
        },
        'datesL1': {
            'stype': 'xpath',
            'value': '//div[@class="css-1ivw6bb-DivCommentSubContentSplitWrapper e1oxncge5"]/div/span[not(@data-e2e="comment-reply-1")]'
            #'value': '//span[@data-e2e="comment-time-1"]'
        },
        'viewMoreBtn': {
            # click on this to start showing replies to level 1 comment
            'stype': 'xpath',
            'value': '//div[@class="css-1idgi02-DivViewRepliesContainer e7fhvc05"]/span[contains(text(), "View")]'
            #'value': '//div[@class="css-zn6r1p-DivReplyContainer eo72wou1"]//p[@role="button" and @data-e2e="view-more-1"]'
        },
        'viewMoreBtnCommentBelongsTo': {
            'stype': 'xpath',
            # the idea of this is to catch only comments that have "View more" button to expand replies
            'value': '//div[@class="css-1idgi02-DivViewRepliesContainer e7fhvc05"]/span[contains(text(), "View")]/../../../../div/div//span[@data-e2e="comment-level-1"]'
        },
        'viewMoreBtnBelongsTo': {
            'stype': 'xpath',
            # the idea of this is to catch only comments that have "View more" button to expand replies
            'value': '//div[@class="css-1idgi02-DivViewRepliesContainer e7fhvc05"]/../../..//div[@data-e2e="comment-username-1"]'
            #'value': '//div[@class="css-zn6r1p-DivReplyContainer eo72wou1"]//p[@role="button" and @data-e2e="view-more-1"]/../../../div//p[@data-e2e="comment-level-1"]'
        },
        'viewMoreBtn2': {
            # click on this to see more replies to level 1 comment
            # keep clicking until it does not appear
            'stype': 'xpath',
            'value': '//div[@class="css-o669do-DivViewMoreRepliesOptionsContainer e7fhvc08"]//span[contains(text(), "more")]' # for this would need to only take the first element found.
            #'value': '//div[@class="css-zn6r1p-DivReplyContainer eo72wou1"]//p[@role="button" and @data-e2e="view-more-2"]'
        },
        'repliesHide': {
            'stype': 'xpath',
            'value': '//div[@class="css-1idgi02-DivViewRepliesContainer e7fhvc05"]/span[contains(text(),"Hide")]' # for this, would need to select the element number corresponding to the desired comment (based on username) 
        },
        'usernameL2': {
            'stype': 'xpath',
            'value': '//div[@class="css-13x3qpp-DivUsernameContentWrapper e1oxncge4" and @data-e2e="comment-username-2"]/div/a',
            #'value': '//div[@class="css-1i7ohvi-DivCommentItemContainer eo72wou0"]//div[@class="css-zn6r1p-DivReplyContainer eo72wou1"]//span[@data-e2e="comment-username-2"]'
        },
        'usernameProfileLinkL2': {
            'stype': 'xpath',
            'value': '//div[@class="css-13x3qpp-DivUsernameContentWrapper e1oxncge4" and @data-e2e="comment-username-2"]/div/a',
            #'value': '//div[@class="css-1i7ohvi-DivCommentItemContainer eo72wou0"]//div[@class="css-zn6r1p-DivReplyContainer eo72wou1"]//span[@data-e2e="comment-username-2"]/..',
        },
        'L2': {
            'stype': 'xpath',
            # take all values but the last which seems to be a ghost...
            'value': '//div[@class="css-1k8xzzl-DivCommentContentWrapper e1oxncge2"]//span[@data-e2e="comment-level-2"]'
            #'value': '//div[@class="css-1i7ohvi-DivCommentItemContainer eo72wou0"]//div[@class="css-zn6r1p-DivReplyContainer eo72wou1"]//p[@data-e2e="comment-level-2"]'
        },
        'likesCountL2': {
            'stype': 'xpath',
            # take all elements but the last
            'value': '//span[@data-e2e="comment-reply-2"]/preceding-sibling::div/span'
            #'value': '//div[@class="css-1i7ohvi-DivCommentItemContainer eo72wou0"]//div[@class="css-zn6r1p-DivReplyContainer eo72wou1"]//span[@data-e2e="comment-like-count"]'
        },
        'datesL2': {
            'stype': 'xpath',
            # take all elements but the last
            'value': '//span[@data-e2e="comment-reply-2"]/../../div/span[1]'
            #'value': '//span[@data-e2e="comment-time-2"]',
        },
        'viewMoreAndHideL2Btns': {
            'stype': 'xpath',
            # this exists only if "View More replies" and "Hide" button exists in the same level
            'value': '//div[@class="css-1idgi02-DivViewRepliesContainer e7fhvc05"]/span[contains(text(),"Hide")]/../../div/span[contains(text(), "more")]'
        },
    },
    'common': {
        'loginContainer': {
            'stype': 'xpath',
            'value': '//*[@id="loginContainer"]'
        }
    }
}
